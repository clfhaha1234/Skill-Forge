"""Evaluate slide images against references using Gemini 3.1 Pro Preview."""

import json
import os
import re

from google import genai
from google.genai import types

EVALUATION_RUBRIC = """You are an expert slide design evaluator.

You will be shown:
1. REFERENCE IMAGES: Gold-standard slides provided by the user. These represent the target visual style.
2. CANDIDATE SLIDE: A programmatically generated slide rendered as a JPEG image.

Score how closely the CANDIDATE SLIDE matches the visual style in the REFERENCE IMAGES.

## Scoring Rubric (100 points total)

### 1. Background & Base Layout (0-15 points)
- Clean background matching reference style
- Proper margins (~0.5" all sides)
- No unnecessary visual clutter

### 2. Color Palette Fidelity (0-15 points)
- Matches reference color palette
- Restrained, professional palette
- Accent colors used sparingly

### 3. Typography (0-15 points)
- Font hierarchy matches reference
- Clear size hierarchy: title >> subtitle >> body >> footnotes

### 4. Title Quality — "So-What" Style (0-15 points)
- Insight-driven conclusion title, not just a topic label
- Title tells the key takeaway without reading the slide

### 5. Data Presentation (0-15 points)
- Data format matches reference style (tables, charts, etc.)
- Organized, scannable, well-structured

### 6. Structural Elements (0-15 points)
- Divider lines, footers, footnotes matching reference
- Source attribution, page numbers present

### 7. Overall Visual Impression (0-10 points)
- Does this feel like it came from the same source as the references?
- Clean, restrained, and authoritative

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


def evaluate_slide(
    slide_image: bytes,
    reference_images: list[bytes],
    api_key: str | None = None,
) -> dict:
    """Score a slide image against reference images using Gemini vision.

    Args:
        slide_image: JPEG bytes of the candidate slide.
        reference_images: List of JPEG bytes for reference slides.
        api_key: Gemini API key (falls back to GEMINI_API_KEY env var).

    Returns:
        Dict with scores, total, strengths, weaknesses, one_line_verdict.
    """
    key = api_key or os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=key)

    parts = []
    parts.append(types.Part.from_text(
        "## REFERENCE IMAGES (Gold standard)\n"
        "Study these reference slides carefully. The candidate should match this style."
    ))
    for i, ref_bytes in enumerate(reference_images):
        parts.append(types.Part.from_bytes(data=ref_bytes, mime_type="image/jpeg"))
        parts.append(types.Part.from_text(f"(Reference {i + 1})"))

    parts.append(types.Part.from_text("\n## CANDIDATE SLIDE TO EVALUATE"))
    parts.append(types.Part.from_bytes(data=slide_image, mime_type="image/jpeg"))
    parts.append(types.Part.from_text(
        "\nScore this candidate against the references using the rubric. "
        "Return ONLY the JSON object."
    ))

    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=[types.Content(role="user", parts=parts)],
        config=types.GenerateContentConfig(
            system_instruction=EVALUATION_RUBRIC,
            temperature=0.2,
            max_output_tokens=1024,
        ),
    )

    text = response.text.strip()
    # Extract JSON from markdown fences if present
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        text = json_match.group(0)
    # Fix trailing commas
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return json.loads(text)
