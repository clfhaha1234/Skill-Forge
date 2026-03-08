"""
Evaluator Adapter — wraps the existing output/evaluator.py logic as a
reusable module with a clean interface.

This module does NOT import output/evaluator.py (which has a __main__ guard
and hardcoded paths). Instead, it re-implements the core evaluate_slide()
logic with:
    - Configurable reference image paths
    - A return type that includes all seven score keys, strengths, weaknesses,
      and one_line_verdict
    - No file I/O side effects (no evaluation_results.json written)

The evaluation prompt is identical to output/evaluator.py so scores are
comparable across the historical runs and the OpenEnv loop.

Note on Gemini vs. Anthropic image handling:
    Gemini's SDK accepts image bytes directly via types.Part.from_bytes(),
    so base64 encoding is not needed here (unlike the Anthropic SDK).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from google import genai
from google.genai import types


# Must match output/evaluator.py exactly so historical scores are comparable.
EVALUATION_SYSTEM_PROMPT = """You are an expert McKinsey & Company slide design evaluator.

You will be shown:
1. REFERENCE IMAGES: 5 pages from a real McKinsey & Company consulting deck (Chilean Hydrogen Pathway, December 2020). These represent the gold standard for visual style.
2. CANDIDATE SLIDE: A programmatically generated PowerPoint slide about Dutch Hydrogen Strategy, rendered as a JPEG image.

Your job: Score how closely the CANDIDATE SLIDE matches the McKinsey visual style shown in the REFERENCE IMAGES.

## Scoring Rubric (100 points total)

### 1. Background & Base Layout (0-15 points)
- McKinsey content/data slides use WHITE backgrounds (dark navy is ONLY for section dividers/covers)
- Clean margins (~0.5" all sides)
- No unnecessary visual clutter
- 15: White bg, clean margins, professional spacing
- 10: White bg but spacing issues
- 5: Wrong background color or major layout problems
- 0: Completely wrong base (e.g., dark bg for data slide)

### 2. Color Palette Fidelity (0-15 points)
- McKinsey uses a RESTRAINED palette: navy/dark blue (#0C2340-ish), white, light greys
- Accent colors are used SPARINGLY — typically just 1-2 accent colors max
- NO rainbow effects, no bright multi-color schemes
- Crimson/red used only for thin divider lines, not large elements
- 15: Matches McKinsey's restrained navy/white/grey palette perfectly
- 10: Mostly correct but 1-2 color choices off
- 5: Too many colors or wrong color family
- 0: Completely different color scheme

### 3. Typography (0-15 points)
- Title: Large, bold, black or very dark, left-aligned (Georgia or similar serif for titles)
- Body: Clean sans-serif (Calibri-like), smaller, grey or dark grey
- Clear size hierarchy: title >> subtitle >> body >> footnotes
- No decorative fonts
- 15: Perfect type hierarchy matching McKinsey
- 10: Good hierarchy but font choices slightly off
- 5: Weak hierarchy or wrong fonts
- 0: No clear hierarchy

### 4. Title Quality — "So-What" Style (0-15 points)
- McKinsey titles state a CONCLUSION or INSIGHT, not just a topic
- GOOD: "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"
- BAD: "Dutch Hydrogen Strategy (2020-2035)" or "Roadmap Overview"
- The title should tell you the key takeaway without reading the slide
- 15: Clear insight-driven conclusion title
- 10: Partial insight (has some specifics but reads more like a topic)
- 5: Pure topic label
- 0: Generic or missing title

### 5. Data Presentation (0-15 points)
- McKinsey uses structured TABLES for data (not floating stat callouts)
- Tables have: navy header borders (top + bottom of header row), light grey row dividers, bold left column labels
- Data should be organized, scannable, center-aligned values
- Key columns/years may be subtly highlighted
- 15: Clean structured table matching McKinsey format
- 10: Has data but format doesn't match McKinsey tables
- 5: Data present but poorly structured (floating callouts, inconsistent format)
- 0: No supporting data

### 6. Structural Elements (0-15 points)
- Thin crimson/red divider line below title area (not touching title — separated by whitespace)
- McKinsey footer: thin rule line + source text (left) + "McKinsey & Company" bold (right) + page number
- Numbered footnotes for data disclaimers
- Source attribution line
- 15: All structural elements present and correctly placed
- 10: Most elements present, minor placement issues
- 5: Missing 2+ structural elements
- 0: No McKinsey structural elements

### 7. Overall Visual Impression (0-10 points)
- Does this FEEL like it came from McKinsey?
- Would a consulting professional find this polished and credible?
- Is it clean, restrained, and authoritative — or busy, colorful, and amateur?
- 10: Indistinguishable from real McKinsey output
- 7: Close but a trained eye spots differences
- 4: Clearly generated/templated but has some McKinsey DNA
- 1: Does not resemble McKinsey at all

## Output Format

Return ONLY a JSON object with this exact structure (no markdown, no code fences):
{
    "scores": {
        "background_layout": <0-15>,
        "color_palette": <0-15>,
        "typography": <0-15>,
        "title_quality": <0-15>,
        "data_presentation": <0-15>,
        "structural_elements": <0-15>,
        "overall_impression": <0-10>
    },
    "total": <sum of all scores, 0-100>,
    "strengths": ["<strength 1>", "<strength 2>", ...],
    "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
    "one_line_verdict": "<one sentence summary>"
}
"""

EVALUATOR_MODEL = "gemini-3.1-pro-preview"


def _image_part(path: Path) -> types.Part:
    """Load an image file as a Gemini Part (bytes + mime type)."""
    suffix = path.suffix.lower()
    mime_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"
    return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type)


class EvaluatorAdapter:
    """
    Adapter that evaluates a generated slide JPG against McKinsey references.

    Uses Gemini 3.1 Pro with vision, replicating the evaluation logic from
    output/evaluator.py as a reusable class with no file I/O side effects.
    """

    REFERENCE_FILENAMES = [
        "ref-01.jpg",
        "ref-02.jpg",
        "ref-03.jpg",
        "ref-04.jpg",
        "ref-05.jpg",
    ]

    def __init__(self, reference_dir: Path) -> None:
        """
        Args:
            reference_dir: Directory containing ref-01.jpg through ref-05.jpg.
        """
        self.reference_dir = reference_dir
        self._client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

        # Validate reference images exist at construction time.
        missing = [
            f
            for f in self.REFERENCE_FILENAMES
            if not (reference_dir / f).exists()
        ]
        if missing:
            raise FileNotFoundError(
                f"Missing reference images in {reference_dir}: {missing}"
            )

    def evaluate(self, slide_jpg_path: Path) -> dict:
        """
        Evaluate a generated slide against the McKinsey reference images.

        Args:
            slide_jpg_path: Absolute path to the slide JPG to evaluate.

        Returns:
            dict with keys:
                "scores": dict mapping the 7 dimension names to int scores
                "total": int, sum of all scores (0-100)
                "strengths": list[str]
                "weaknesses": list[str]
                "one_line_verdict": str

        Raises:
            FileNotFoundError: If slide_jpg_path does not exist.
            json.JSONDecodeError: If the LLM returns malformed JSON.
            RuntimeError: If the API call fails.
        """
        if not slide_jpg_path.exists():
            raise FileNotFoundError(f"Slide JPG not found: {slide_jpg_path}")

        # Build a flat list of Parts for the Gemini content parameter.
        # Gemini accepts text strings and Part objects interleaved.
        contents: list[types.Part | str] = []

        # Reference images first.
        contents.append(
            "## REFERENCE IMAGES (Real McKinsey deck)\n"
            "The following 5 images are from a real McKinsey & Company consulting "
            "report. Study their visual style carefully."
        )
        for i, fname in enumerate(self.REFERENCE_FILENAMES, 1):
            contents.append(_image_part(self.reference_dir / fname))
            contents.append(f"(Reference page {i})")

        # Candidate slide.
        contents.append(
            f"\n## CANDIDATE SLIDE TO EVALUATE\n"
            f"This is the generated slide: {slide_jpg_path.name}"
        )
        contents.append(_image_part(slide_jpg_path))
        contents.append(
            "\nNow score this candidate slide against the McKinsey reference "
            "using the rubric. Return ONLY the JSON object."
        )

        response = self._client.models.generate_content(
            model=EVALUATOR_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=EVALUATION_SYSTEM_PROMPT,
                max_output_tokens=2048,
            ),
        )

        text = response.text.strip()

        # Extract JSON object robustly (handles markdown fences and surrounding text).
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            text = json_match.group(0)

        result = json.loads(text)

        # Validate required keys are present.
        required_score_keys = {
            "background_layout",
            "color_palette",
            "typography",
            "title_quality",
            "data_presentation",
            "structural_elements",
            "overall_impression",
        }
        missing_keys = required_score_keys - set(result.get("scores", {}).keys())
        if missing_keys:
            raise ValueError(
                f"Evaluator response missing score keys: {missing_keys}. "
                f"Full response: {text[:500]}"
            )

        return result
