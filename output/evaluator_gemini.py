#!/usr/bin/env python3
"""
PPT Slide Evaluator (Gemini) — Uses Gemini 3.1 Pro to score generated slides
against McKinsey reference images.

Usage:
    python3 evaluator_gemini.py                          # Evaluate all v0-v5
    python3 evaluator_gemini.py slide_v3-1.jpg           # Evaluate single slide

Output: evaluation_results_gemini.json
"""

from google import genai
from google.genai import types
import json
import re
import sys
from pathlib import Path

# Load API key from .env
ENV_PATH = Path(__file__).parent.parent / ".env"
GEMINI_API_KEY = None
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            GEMINI_API_KEY = line.split("=", 1)[1].strip()
if not GEMINI_API_KEY:
    import os
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

MODEL = "gemini-3.1-pro-preview"

OUTPUT_DIR = Path(__file__).parent

REFERENCE_IMAGES = [
    OUTPUT_DIR / "reference" / "ref-01.jpg",
    OUTPUT_DIR / "reference" / "ref-02.jpg",
    OUTPUT_DIR / "reference" / "ref-03.jpg",
    OUTPUT_DIR / "reference" / "ref-04.jpg",
    OUTPUT_DIR / "reference" / "ref-05.jpg",
]

EVALUATION_PROMPT = """You are an expert McKinsey & Company slide design evaluator.

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
- Thin divider line below title area (not touching title — separated by whitespace)
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

You MUST return ONLY a valid JSON object. No explanation, no markdown fences, no extra text.
The JSON must have this exact structure:
{"scores":{"background_layout":0,"color_palette":0,"typography":0,"title_quality":0,"data_presentation":0,"structural_elements":0,"overall_impression":0},"total":0,"strengths":["..."],"weaknesses":["..."],"one_line_verdict":"..."}
"""


def evaluate_slide(client: genai.Client, slide_path: Path) -> dict:
    """Send reference + candidate images to Gemini and get structured scores."""
    parts = []

    parts.append(types.Part.from_text(text="## REFERENCE IMAGES (Real McKinsey deck)\nThe following 5 images are from a real McKinsey & Company consulting report. Study their visual style carefully."))

    for i, ref_path in enumerate(REFERENCE_IMAGES, 1):
        if ref_path.exists():
            parts.append(types.Part.from_bytes(data=ref_path.read_bytes(), mime_type="image/jpeg"))
            parts.append(types.Part.from_text(text=f"(Reference page {i})"))

    parts.append(types.Part.from_text(text=f"\n## CANDIDATE SLIDE TO EVALUATE\nThis is the generated slide: {slide_path.name}"))
    parts.append(types.Part.from_bytes(data=slide_path.read_bytes(), mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text="\nNow score this candidate slide against the McKinsey reference using the rubric. Return ONLY the JSON object, nothing else."))

    response = client.models.generate_content(
        model=MODEL,
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            system_instruction=EVALUATION_PROMPT,
            max_output_tokens=2048,
            temperature=0.2,
        ),
    )

    # Get text from response, handling thought_signature parts
    text = ""
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            text += part.text
    text = text.strip()

    # Handle markdown code fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    # Try to extract JSON from response
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        text = json_match.group(0)

    return json.loads(text)


def main():
    if len(sys.argv) > 1:
        slide_paths = [OUTPUT_DIR / arg for arg in sys.argv[1:]]
    else:
        slide_paths = [OUTPUT_DIR / f"slide_v{i}-1.jpg" for i in range(6)]

    missing = [p for p in slide_paths if not p.exists()]
    if missing:
        print(f"ERROR: Missing files: {[str(p) for p in missing]}")
        sys.exit(1)

    ref_missing = [p for p in REFERENCE_IMAGES if not p.exists()]
    if ref_missing:
        print(f"ERROR: Missing reference images: {[str(p) for p in ref_missing]}")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    results = {}
    for slide_path in slide_paths:
        name = slide_path.stem
        version = name.split("_")[1].split("-")[0]
        print(f"Evaluating {version} ({slide_path.name})...", flush=True)

        try:
            evaluation = evaluate_slide(client, slide_path)
            results[version] = evaluation
            print(f"  {version}: {evaluation['total']}/100 — {evaluation['one_line_verdict']}")
        except Exception as e:
            print(f"  ERROR evaluating {version}: {e}")
            results[version] = {"error": str(e)}

    output_path = OUTPUT_DIR / "evaluation_results_gemini.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    if any("total" in v for v in results.values()):
        print("\n" + "=" * 60)
        print(f"{'Version':<10} {'Score':<8} {'Verdict'}")
        print("-" * 60)
        for version in sorted(results.keys()):
            r = results[version]
            if "total" in r:
                print(f"{version:<10} {r['total']:<8} {r['one_line_verdict']}")
            else:
                print(f"{version:<10} {'ERROR':<8} {r.get('error', 'unknown')}")
        print("=" * 60)


if __name__ == "__main__":
    main()
