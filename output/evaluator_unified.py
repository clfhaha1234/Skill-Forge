#!/usr/bin/env python3
"""
Unified PPT Slide Evaluator — Patronus gate + Gemini fine-grained scoring.

Flow:
  1. Patronus Judge MM: binary pass/fail on 8 McKinsey criteria
     → If FAIL: outputs exactly which criteria failed (actionable for optimizer)
     → If PASS: proceeds to step 2
  2. Gemini 3.1 Pro: 0-100 fine-grained scoring with rubric
     → Only runs if Patronus passes (saves API cost on obvious failures)

Usage:
    python3 evaluator_unified.py                    # Evaluate all v0-v5
    python3 evaluator_unified.py slide_v3-1.jpg     # Evaluate single slide
    python3 evaluator_unified.py --all              # Force Gemini on all, even failures

Output: evaluation_unified.json
"""

import base64
import json
import re
import sys
import os
import urllib.request
from pathlib import Path

# ── Config ──────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent
ENV_PATH = OUTPUT_DIR.parent / ".env"

# Load .env
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

PATRONUS_API_KEY = os.environ.get("PATRONUS_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

PATRONUS_CRITERIA = "mckinsey-slide-eval:1"
GEMINI_MODEL = "gemini-3.1-pro-preview"

REFERENCE_IMAGES = [
    OUTPUT_DIR / "reference" / "ref-01.jpg",
    OUTPUT_DIR / "reference" / "ref-02.jpg",
    OUTPUT_DIR / "reference" / "ref-03.jpg",
    OUTPUT_DIR / "reference" / "ref-04.jpg",
    OUTPUT_DIR / "reference" / "ref-05.jpg",
]

# ── Patronus Gate ───────────────────────────────────────────

def upload_image(path: Path) -> str:
    """Upload image to tmpfiles.org via curl and return direct download URL."""
    import subprocess
    result = subprocess.run(
        ["curl", "-s", "-F", f"file=@{path}", "https://tmpfiles.org/api/v1/upload"],
        capture_output=True, text=True, timeout=30,
    )
    data = json.loads(result.stdout)
    url = data["data"]["url"]
    return url.replace("tmpfiles.org/", "tmpfiles.org/dl/")


def patronus_evaluate(slide_path: Path) -> dict:
    """Run Patronus Judge MM pass/fail evaluation."""
    image_url = upload_image(slide_path)

    payload = json.dumps({
        "evaluators": [{
            "evaluator": "judge-image-large",
            "criteria": PATRONUS_CRITERIA,
            "explain_strategy": "always",
        }],
        "task_input": "Evaluate this generated PowerPoint slide for McKinsey & Company consulting visual style quality.",
        "task_output": "Generated PowerPoint slide about Dutch Hydrogen Strategy timeline",
        "evaluated_model_attachments": [
            {"url": image_url, "media_type": "image/jpeg"}
        ],
    }).encode()

    req = urllib.request.Request(
        "https://api.patronus.ai/v1/evaluate",
        data=payload,
        headers={
            "X-API-KEY": PATRONUS_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    r = data["results"][0]

    if r["status"] != "success":
        return {"pass": False, "error": r.get("error_message", "unknown"), "criteria_results": [], "explanation": ""}

    ev = r["evaluation_result"]
    explanation = ev.get("explanation", "")

    # Parse per-criterion results from explanation
    criteria_results = parse_criteria(explanation)

    return {
        "pass": ev["pass"],
        "explanation": explanation,
        "criteria_results": criteria_results,
        "failed_criteria": [c for c in criteria_results if not c["met"]],
    }


def parse_criteria(explanation: str) -> list:
    """Parse Patronus explanation into structured per-criterion results."""
    criteria_names = [
        "White background",
        "Restrained color palette",
        "Insight-driven title",
        "Structured data table",
        "Proper McKinsey footer",
        "Clean typography hierarchy",
        "Thin divider line",
        "Professional polish",
    ]
    results = []
    text = explanation.lower()
    for i, name in enumerate(criteria_names, 1):
        # Look for MET/NOT MET/FAIL/PASS patterns near the criterion
        met = True
        search_area = text
        # Try to find this criterion's section
        for marker in [f"({i})", f"**({i})", f"{i}.", f"criterion {i}", f"**{i}"]:
            idx = search_area.find(marker)
            if idx >= 0:
                # Get text from this criterion to the next one or end
                end = len(search_area)
                for next_marker in [f"({i+1})", f"**({i+1})", f"{i+1}.", f"criterion {i+1}"]:
                    nidx = search_area.find(next_marker, idx + 1)
                    if nidx >= 0:
                        end = min(end, nidx)
                section = search_area[idx:end]
                if "not met" in section or "not fulfilled" in section or "fail" in section or "is not met" in section:
                    met = False
                break
        results.append({"criterion": name, "index": i, "met": met})
    return results


# ── Gemini Fine-Grained Scoring ────────────────────────────

GEMINI_SYSTEM_PROMPT = """You are an expert McKinsey & Company slide design evaluator.

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


def gemini_evaluate(slide_path: Path) -> dict:
    """Run Gemini fine-grained 0-100 scoring."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=GEMINI_API_KEY)

    parts = []
    parts.append(types.Part.from_text(text="## REFERENCE IMAGES (Real McKinsey deck)"))
    for i, ref_path in enumerate(REFERENCE_IMAGES, 1):
        if ref_path.exists():
            parts.append(types.Part.from_bytes(data=ref_path.read_bytes(), mime_type="image/jpeg"))
            parts.append(types.Part.from_text(text=f"(Reference page {i})"))

    parts.append(types.Part.from_text(text=f"\n## CANDIDATE SLIDE: {slide_path.name}"))
    parts.append(types.Part.from_bytes(data=slide_path.read_bytes(), mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text="\nScore this slide. Return ONLY JSON."))

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            system_instruction=GEMINI_SYSTEM_PROMPT,
            max_output_tokens=2048,
            temperature=0.2,
        ),
    )

    text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            text += part.text
    text = text.strip()

    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        text = json_match.group(0)

    return json.loads(text)


# ── Main ────────────────────────────────────────────────────

def main():
    force_all = "--all" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        slide_paths = [OUTPUT_DIR / a for a in args]
    else:
        slide_paths = [OUTPUT_DIR / f"slide_v{i}-1.jpg" for i in range(6)]

    missing = [p for p in slide_paths if not p.exists()]
    if missing:
        print(f"ERROR: Missing files: {[str(p) for p in missing]}")
        sys.exit(1)

    results = {}
    for slide_path in slide_paths:
        name = slide_path.stem
        version = name.split("_")[1].split("-")[0]

        print(f"\n{'='*50}")
        print(f"  {version} — {slide_path.name}")
        print(f"{'='*50}")

        # Step 1: Patronus gate
        print(f"  [1/2] Patronus gate...", flush=True)
        try:
            patronus = patronus_evaluate(slide_path)
            gate_pass = patronus["pass"]
            failed = patronus.get("failed_criteria", [])
            if gate_pass:
                print(f"        ✓ PASS (all 8 criteria met)")
            else:
                print(f"        ✗ FAIL ({len(failed)} criteria not met):")
                for c in failed:
                    print(f"          - [{c['index']}] {c['criterion']}")
        except Exception as e:
            print(f"        ERROR: {e}")
            patronus = {"pass": False, "error": str(e), "criteria_results": [], "failed_criteria": []}
            gate_pass = False

        # Step 2: Gemini scoring (only if passed gate, or --all flag)
        gemini_result = None
        if gate_pass or force_all:
            print(f"  [2/2] Gemini scoring...", flush=True)
            try:
                gemini_result = gemini_evaluate(slide_path)
                print(f"        Score: {gemini_result['total']}/100 — {gemini_result['one_line_verdict']}")
            except Exception as e:
                print(f"        ERROR: {e}")
                gemini_result = {"error": str(e)}
        else:
            print(f"  [2/2] Gemini scoring... SKIPPED (gate failed)")

        # Combine results
        results[version] = {
            "patronus_gate": {
                "pass": patronus["pass"],
                "criteria_results": patronus.get("criteria_results", []),
                "failed_criteria": [c["criterion"] for c in patronus.get("failed_criteria", [])],
            },
            "gemini_score": gemini_result,
            "final_status": "PASS" if gate_pass else "FAIL",
            "final_score": gemini_result["total"] if gemini_result and "total" in gemini_result else None,
            "action_items": [
                f"Fix: {c['criterion']}" for c in patronus.get("failed_criteria", [])
            ],
        }

    # Save
    output_path = OUTPUT_DIR / "evaluation_unified.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    # Summary table
    print(f"\n{'='*70}")
    print(f"{'Version':<8} {'Gate':<8} {'Score':<8} {'Action Items'}")
    print(f"{'-'*70}")
    for v in sorted(results.keys()):
        r = results[v]
        gate = "PASS" if r["final_status"] == "PASS" else "FAIL"
        score = str(r["final_score"]) if r["final_score"] else "—"
        actions = "; ".join(r["action_items"]) if r["action_items"] else "None"
        print(f"{v:<8} {gate:<8} {score:<8} {actions}")
    print(f"{'='*70}")
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
