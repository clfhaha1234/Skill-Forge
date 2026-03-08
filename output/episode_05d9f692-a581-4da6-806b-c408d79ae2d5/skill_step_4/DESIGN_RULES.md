# McKinsey-Style Slide Design Rules

## Slide Dimensions & Zones
- Slide: 10" wide × 7.5" tall
- All positions use 0.5" margins

| Zone | Y Position | Content |
|------|-----------|---------|
| Title | y=0.4"–1.1" | Insight title, 20pt Georgia bold, navy `#003A70` |
| Divider | y=1.2" | 1pt grey `#CCCCCC` line, x=0.5" to x=9.5" |
| Body | y=1.4"–6.4" | Tables, charts, diagrams |
| Source | y=6.75" | "Source: ...; McKinsey analysis" — 8pt `#666666` left-aligned |
| Footer line | y=6.9" | 0.75pt grey `#CCCCCC` line |
| Footer | y=7.0" | "CONFIDENTIAL" (left) + "McKinsey & Company  1" (right) — 8pt `#666666` |

## Color Palette (3 colors only)
| Use | Color | Hex |
|-----|-------|-----|
| Title text, table header text, header borders | Navy | `#003A70` |
| Body text | Dark grey | `#333333` |
| Labels, source, footer text | Medium grey | `#666666` |
| Accent (sparingly) | McKinsey blue | `#0072CE` |
| All backgrounds | White | `#FFFFFF` |
| Table header fill | Light grey | `#F2F2F2` |
| Internal gridlines, dividers | Light grey | `#D9D9D9` |
| **BANNED** | Teal, cyan, seafoam, mint, bright green, orange | — |

## Typography
| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Title | Georgia | 18–22pt | Bold | `#003A70` |
| Section headers | Calibri/Arial | 12–14pt | Bold | `#003A70` |
| Body text | Calibri/Arial | 10–12pt | Regular | `#333333` |
| Table header | Calibri/Arial | 11pt | Bold | `#003A70` |
| Table data | Calibri/Arial | 10–11pt | Regular | `#333333` |
| Small labels (boxes) | Calibri/Arial | 9–10pt | Regular | `#333333` |
| Source & footer | Calibri/Arial | 8pt | Regular | `#666666` |

## Title Rules
- Must be an insight-driven "so-what" statement, NOT a topic label
- Formula: [Subject] + [verb] + [quantified outcome]
- ❌ "Dutch Hydrogen Strategy" → ✅ "Three H₂ corridors could position NL as Europe's hub by 2030"
- Max 120 characters; keep to 1–2 lines at 20pt
- Text box: x=0.5", y=0.4", width=8.5", height=0.7"
- Must NOT extend below y=1.1" (0.1" gap before divider at y=1.2")
- Shorten with: "NL" not "Netherlands", symbols (€, %, →), drop filler words

## Footer (MANDATORY — All 4 Elements Required)
1. **Source** at y=6.75": `Source: [description]; McKinsey analysis` — 8pt grey, left-aligned
2. **Footer line** at y=6.9": thin grey rule spanning full width
3. **"CONFIDENTIAL"** at y=7.0", x=0.5": 8pt grey, left-aligned
4. **"McKinsey & Company  1"** at y=7.0", right-aligned to x=9.5": 8pt grey

⚠️ Missing "McKinsey & Company" = automatic FAIL.

## Table Styling — McKinsey Border Hierarchy
Tables MUST use differentiated borders, NOT uniform gridlines:

| Border | Weight | Color | Required? |
|--------|--------|-------|-----------|
| Header row bottom | **2pt** | Navy `#003A70` | **YES — signature element** |
| Table bottom (last row) | 1pt | Navy `#003A70` | Yes |
| Header row top | 1pt | Navy `#003A70` | Optional |
| Internal row separators | 0.5pt | Light grey `#D9D9D9` | Yes |
| Vertical gridlines | 0.5pt or NONE | `#D9D9D9` | Prefer NONE |
| Left/right outer edges | NONE | — | No outer borders |

**Header row**: `#F2F2F2` fill, navy bold text, 2pt navy bottom border
**Data rows**: white fill, `#333333` text, 0.5pt grey separators
**Alignment**: text left-aligned, numbers right-aligned
**Cell padding**: 0.05" min; row height: 0.35" min

❌ Never use uniform-weight borders (looks like Excel)
❌ Never use colored cell fills (teal, blue, green)
❌ Never use heavy outer box borders

## Layout Rules
- Body content MUST stay between y=1.4" and y=6.4"
- Min 0.15" gap between any two elements
- Boxes: thin borders (0.75pt) light grey, NO solid colored fills
- No element may overlap another element
- White space is intentional — at least 30% of body area

## Text Fitting (NO TRUNCATION EVER)
- Size containers to fit text, not text to fit containers
- Use short labels (2–4 words) inside small boxes; details outside/below
- Enable word_wrap=True; use MSO_AUTO_SIZE.NONE
- Min box size: 1.2"W × 0.5"H (single line), 1.5"W × 0.7"H (timeline boxes)
- If >5 horizontal boxes, switch to vertical layout or reduce phases
- Never go below 8pt for any text

## Timeline/Process Layout
- ≤4 phases: horizontal row, each box = (9.0 - gaps) / N inches wide
- 5–7 phases: 9pt font, abbreviated labels, or 2-row stacked layout
- >7 phases: vertical list format
- Short labels inside boxes; detailed text BELOW boxes
- NO icons inside boxes — text only

## What to AVOID
- ❌ Text truncation ("Hydrog..." = FAIL)
- ❌ Overlapping elements
- ❌ Missing "McKinsey & Company" footer
- ❌ Dark/colored backgrounds
- ❌ Solid-colored box fills
- ❌ Uniform table borders (Excel-style)
- ❌ Title as topic label ("Market Overview")
- ❌ Title font >22pt (causes overflow)
- ❌ Content below y=6.4"
- ❌ Source text floating high (must be at y=6.75")
- ❌ Icons overlapping text
