"""Evaluate slide images against references using Patronus gate + Gemini scoring.

Flow:
  1. Patronus Judge MM: binary pass/fail on McKinsey criteria (8 checkpoints)
     → If FAIL: returns failed criteria as actionable weaknesses
     → If PASS: proceeds to Gemini scoring
  2. Gemini 3.1 Pro: 0-100 fine-grained scoring with rubric

Patronus is the primary quality gate; Gemini provides the fine-grained score.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
import urllib.request

from google import genai
from google.genai import types

EVALUATION_RUBRIC = """You are an expert McKinsey & Company slide design evaluator.

You will be shown reference images from a real McKinsey deck, then a candidate slide to score.

## Scoring Rubric (100 points total)

1. Background & Layout (0-15): White bg, clean margins, no clutter
2. Color Palette (0-15): Restrained navy/white/grey, no rainbow
3. Typography (0-15): Serif title, sans-serif body, clear hierarchy
4. Title Quality (0-15): Insight-driven "so-what" conclusion, not topic label
5. Data Presentation (0-15): Structured table with navy header borders
6. Structural Elements (0-15): Divider line, footer, footnotes, source
7. Overall Impression (0-10): Does it feel like real McKinsey output?

Return ONLY valid JSON:
{"scores":{"background_layout":0,"color_palette":0,"typography":0,"title_quality":0,"data_presentation":0,"structural_elements":0,"overall_impression":0},"total":0,"strengths":["..."],"weaknesses":["..."],"one_line_verdict":"..."}"""


PATRONUS_CRITERIA = "mckinsey-slide-eval:1"
PATRONUS_CRITERIA_NAMES = [
    "White background",
    "Restrained color palette",
    "Insight-driven title",
    "Structured data table",
    "Proper McKinsey footer",
    "Clean typography hierarchy",
    "Thin divider line",
    "Professional polish",
]


def _upload_image_for_patronus(image_bytes: bytes) -> str:
    """Write image to temp file and upload to tmpfiles.org for Patronus."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        f.write(image_bytes)
        tmp_path = f.name
    try:
        result = subprocess.run(
            ["curl", "-s", "-F", f"file=@{tmp_path}", "https://tmpfiles.org/api/v1/upload"],
            capture_output=True, text=True, timeout=30,
        )
        data = json.loads(result.stdout)
        url = data["data"]["url"]
        return url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    finally:
        os.unlink(tmp_path)


def _parse_patronus_criteria(explanation: str) -> list[dict]:
    """Parse Patronus explanation into per-criterion pass/fail results."""
    results = []
    text = explanation.lower()
    for i, name in enumerate(PATRONUS_CRITERIA_NAMES, 1):
        met = True
        for marker in [f"({i})", f"**({i})", f"{i}.", f"criterion {i}", f"**{i}"]:
            idx = text.find(marker)
            if idx >= 0:
                end = len(text)
                for next_marker in [f"({i+1})", f"**({i+1})", f"{i+1}.", f"criterion {i+1}"]:
                    nidx = text.find(next_marker, idx + 1)
                    if nidx >= 0:
                        end = min(end, nidx)
                section = text[idx:end]
                if any(kw in section for kw in ["not met", "not fulfilled", "fail", "is not met"]):
                    met = False
                break
        results.append({"criterion": name, "index": i, "met": met})
    return results


def patronus_evaluate(slide_image: bytes, api_key: str | None = None) -> dict:
    """Run Patronus Judge MM pass/fail evaluation on a slide image.

    Returns:
        Dict with 'pass' (bool), 'criteria_results', 'failed_criteria',
        'explanation'.
    """
    key = api_key or os.environ.get("PATRONUS_API_KEY", "")
    if not key:
        return {"pass": True, "criteria_results": [], "failed_criteria": [],
                "explanation": "PATRONUS_API_KEY not set — skipped"}

    image_url = _upload_image_for_patronus(slide_image)

    payload = json.dumps({
        "evaluators": [{
            "evaluator": "judge-image-large",
            "criteria": PATRONUS_CRITERIA,
            "explain_strategy": "always",
        }],
        "task_input": "Evaluate this generated PowerPoint slide for McKinsey & Company consulting visual style quality.",
        "task_output": "Generated PowerPoint slide",
        "evaluated_model_attachments": [
            {"url": image_url, "media_type": "image/jpeg"}
        ],
    }).encode()

    req = urllib.request.Request(
        "https://api.patronus.ai/v1/evaluate",
        data=payload,
        headers={
            "X-API-KEY": key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    r = data["results"][0]

    if r["status"] != "success":
        return {"pass": False, "error": r.get("error_message", "unknown"),
                "criteria_results": [], "failed_criteria": [], "explanation": ""}

    ev = r["evaluation_result"]
    explanation = ev.get("explanation", "")
    criteria_results = _parse_patronus_criteria(explanation)
    failed = [c for c in criteria_results if not c["met"]]

    return {
        "pass": ev["pass"],
        "explanation": explanation,
        "criteria_results": criteria_results,
        "failed_criteria": failed,
    }


def evaluate_slide(
    slide_image: bytes,
    reference_images: list[bytes],
    api_key: str | None = None,
    patronus_api_key: str | None = None,
    skip_patronus: bool = False,
) -> dict:
    """Score a slide image using Patronus gate + Gemini fine-grained scoring.

    Args:
        slide_image: JPEG bytes of the candidate slide.
        reference_images: List of JPEG bytes for reference slides.
        api_key: Gemini API key (falls back to GEMINI_API_KEY env var).
        patronus_api_key: Patronus API key (falls back to PATRONUS_API_KEY env var).
        skip_patronus: If True, skip Patronus gate and only run Gemini.

    Returns:
        Dict with scores, total, strengths, weaknesses, one_line_verdict,
        and patronus_gate (pass/fail + criteria details).
    """
    # Step 1: Patronus gate
    patronus_result = {"pass": True, "criteria_results": [], "failed_criteria": []}
    if not skip_patronus:
        try:
            patronus_result = patronus_evaluate(slide_image, api_key=patronus_api_key)
        except Exception as e:
            patronus_result = {"pass": False, "error": str(e),
                               "criteria_results": [], "failed_criteria": []}

    # Step 2: Gemini fine-grained scoring (always run for score, even if gate fails)
    key = api_key or os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=key)

    parts = []
    parts.append(types.Part.from_text(
        text="## REFERENCE IMAGES (Gold standard)\n"
        "Study these reference slides carefully. The candidate should match this style."
    ))
    for i, ref_bytes in enumerate(reference_images):
        parts.append(types.Part.from_bytes(data=ref_bytes, mime_type="image/jpeg"))
        parts.append(types.Part.from_text(text=f"(Reference {i + 1})"))

    parts.append(types.Part.from_text(text="\n## CANDIDATE SLIDE TO EVALUATE"))
    parts.append(types.Part.from_bytes(data=slide_image, mime_type="image/jpeg"))
    parts.append(types.Part.from_text(
        text="\nScore this candidate against the references using the rubric. "
        "Return ONLY the JSON object."
    ))

    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            system_instruction=EVALUATION_RUBRIC,
            temperature=0.2,
            max_output_tokens=4096,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "scores": {
                        "type": "object",
                        "properties": {
                            "background_layout": {"type": "integer"},
                            "color_palette": {"type": "integer"},
                            "typography": {"type": "integer"},
                            "title_quality": {"type": "integer"},
                            "data_presentation": {"type": "integer"},
                            "structural_elements": {"type": "integer"},
                            "overall_impression": {"type": "integer"},
                        },
                        "required": ["background_layout", "color_palette", "typography",
                                     "title_quality", "data_presentation",
                                     "structural_elements", "overall_impression"],
                    },
                    "total": {"type": "integer"},
                    "strengths": {"type": "array", "items": {"type": "string"}},
                    "weaknesses": {"type": "array", "items": {"type": "string"}},
                    "one_line_verdict": {"type": "string"},
                },
                "required": ["scores", "total", "strengths", "weaknesses", "one_line_verdict"],
            },
        ),
    )

    text = response.text.strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {
            "scores": {},
            "total": 0,
            "strengths": [],
            "weaknesses": [f"Evaluator returned invalid JSON: {text[:200]}"],
            "one_line_verdict": "Evaluation parse error",
        }

    # Merge Patronus gate results into the response
    result["patronus_gate"] = {
        "pass": patronus_result.get("pass", True),
        "criteria_results": patronus_result.get("criteria_results", []),
        "failed_criteria": [
            c["criterion"] for c in patronus_result.get("failed_criteria", [])
        ],
    }

    # If Patronus failed, add failed criteria as weaknesses
    if not patronus_result.get("pass", True):
        failed_names = result["patronus_gate"]["failed_criteria"]
        for name in failed_names:
            weakness = f"[Patronus FAIL] {name}"
            if weakness not in result.get("weaknesses", []):
                result.setdefault("weaknesses", []).append(weakness)

    return result
