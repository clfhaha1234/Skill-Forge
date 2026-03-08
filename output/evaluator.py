#!/usr/bin/env python3
"""
PPT Slide Evaluator — Uses Claude Opus 4.6 to score generated slides
against McKinsey reference images.

Usage:
    python3 evaluator.py                          # Evaluate all v0-v5
    python3 evaluator.py slide_v3-1.jpg           # Evaluate single slide
    python3 evaluator.py slide_v3-1.jpg slide_v5-1.jpg  # Evaluate specific slides

Output: evaluation_results.json (and prints summary to stdout)

Requires: ANTHROPIC_API_KEY environment variable
"""

import anthropic
import base64
import json
import sys
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

# Reference images to include in every evaluation call
REFERENCE_IMAGES = [
    OUTPUT_DIR / "reference" / "ref-01.jpg",   # Cover page
    OUTPUT_DIR / "reference" / "ref-02.jpg",   # Content page
    OUTPUT_DIR / "reference" / "ref-03.jpg",   # Data/chart page
    OUTPUT_DIR / "reference" / "ref-04.jpg",   # Data/chart page
    OUTPUT_DIR / "reference" / "ref-05.jpg",   # Content page
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


def encode_image(path: Path) -> dict:
    """Encode an image file to base64 for the Anthropic API."""
    data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    suffix = path.suffix.lower()
    media_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": data,
        },
    }


def evaluate_slide(client: anthropic.Anthropic, slide_path: Path) -> dict:
    """Send reference + candidate images to Claude and get structured scores."""
    # Build content array: reference images first, then the candidate
    content = []

    content.append({"type": "text", "text": "## REFERENCE IMAGES (Real McKinsey deck)\nThe following 5 images are from a real McKinsey & Company consulting report. Study their visual style carefully."})

    for i, ref_path in enumerate(REFERENCE_IMAGES, 1):
        if ref_path.exists():
            content.append(encode_image(ref_path))
            content.append({"type": "text", "text": f"(Reference page {i})"})

    content.append({"type": "text", "text": f"\n## CANDIDATE SLIDE TO EVALUATE\nThis is the generated slide: {slide_path.name}"})
    content.append(encode_image(slide_path))

    content.append({"type": "text", "text": "\nNow score this candidate slide against the McKinsey reference using the rubric. Return ONLY the JSON object."})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=EVALUATION_PROMPT,
        messages=[{"role": "user", "content": content}],
    )

    # Parse JSON from response
    text = response.content[0].text.strip()
    # Handle potential markdown code fences
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def main():
    # Determine which slides to evaluate
    if len(sys.argv) > 1:
        slide_paths = [OUTPUT_DIR / arg for arg in sys.argv[1:]]
    else:
        # Default: evaluate all v0-v5
        slide_paths = [OUTPUT_DIR / f"slide_v{i}-1.jpg" for i in range(6)]

    # Verify files exist
    missing = [p for p in slide_paths if not p.exists()]
    if missing:
        print(f"ERROR: Missing files: {[str(p) for p in missing]}")
        sys.exit(1)

    ref_missing = [p for p in REFERENCE_IMAGES if not p.exists()]
    if ref_missing:
        print(f"ERROR: Missing reference images: {[str(p) for p in ref_missing]}")
        sys.exit(1)

    client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

    results = {}
    for slide_path in slide_paths:
        name = slide_path.stem  # e.g., "slide_v3-1"
        version = name.split("_")[1].split("-")[0]  # e.g., "v3"
        print(f"Evaluating {version} ({slide_path.name})...", flush=True)

        try:
            evaluation = evaluate_slide(client, slide_path)
            results[version] = evaluation
            print(f"  {version}: {evaluation['total']}/100 — {evaluation['one_line_verdict']}")
        except Exception as e:
            print(f"  ERROR evaluating {version}: {e}")
            results[version] = {"error": str(e)}

    # Save results
    output_path = OUTPUT_DIR / "evaluation_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    # Print summary table
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
