# McKinsey-Style Slide Design Rules

## ⚠️ TOP 3 CRITICAL RULES (Most Common Failures)
1. **NO TEXT TRUNCATION** — Every text string must be fully visible. Never let text get cut off (e.g., "National Hydrog..." is UNACCEPTABLE). Size containers to fit text, reduce font size, or use shorter labels. See TEXT_FITTING_RULES.md.
2. **NO OVERLAPPING ELEMENTS** — Title must not overlap divider. Icons must not overlap text. Source must not overlap content. Footer must not overlap source. Every element needs clear spacing. See LAYOUT_PATTERNS.md.
3. **STRUCTURED DATA TABLE REQUIRED** — When presenting data, use a proper table with gridlines, header row, and cell structure. Free-floating text boxes for data = FAIL. See LAYOUT_PATTERNS.md.

## CRITICAL DESIGN PRINCIPLES
1. **White background** — ALWAYS use a clean white (`FFFFFF`) background. Never use dark backgrounds.
2. **Insight-driven title** — The title must be a "so-what" statement, NOT a topic label. Keep it under 120 characters so it fits in 1–2 lines at 18–22pt.
3. **Minimalist, restrained design** — Less is more. Avoid heavy graphics, thick borders, and solid-filled boxes. Use white space generously.
4. **Professional polish** — Every element must be precisely aligned, consistently spaced, and purposefully placed. Zero overlaps, zero truncation.
5. **Proper McKinsey footer** — Every slide MUST have: source attribution, footer divider line, "CONFIDENTIAL" (left), page number (right). This is auto-checked.

## Color Palette (MANDATORY — McKinsey Brand)
- **Primary text**: Dark navy `#003A70` or near-black `#1A1A2E`
- **Secondary text / labels**: Medium grey `#666666` or `#58595B`
- **Accent (sparingly)**: McKinsey blue `#0072CE` — used only for key highlights
- **Backgrounds**: Pure white `#FFFFFF` only
- **Borders / lines**: Light grey `#CCCCCC` or `#D9D9D9`
- **Table header fill**: Very light grey `#F2F2F2`
- **DO NOT USE**: Teal, cyan, seafoam, mint, bright green, or any saturated/vibrant colors
- Keep the palette to 3 colors maximum: navy, grey, and white

## Typography
- **Title**: Georgia or similar serif font, **18–22pt**, bold, dark navy `#003A70`
  - ⚠️ Do NOT use 24–28pt — this causes overflow/wrapping on long insight titles
  - Title text box: 8.5" wide, starting at x=0.5", y=0.4"
  - Must not extend below y=1.1" on the slide
- **Subtitle / section headers**: Calibri or Arial, 12–14pt, bold, dark navy or dark grey
- **Body text**: Calibri or Arial, 10–12pt, regular, dark grey `#333333`
- **Small box labels**: Calibri or Arial, **9–10pt** — use this for timeline boxes and compact elements
- **Source / footnote text**: Calibri or Arial, 8–9pt, regular, medium grey `#666666`
- **Numbers / data**: Calibri or Arial, can be bold for emphasis

## Mandatory Structural Elements

### Thin Divider Line Under Title
- Position: y=1.2", from x=0.5" to x=9.5"
- Style: 0.75–1pt weight, light grey `#CCCCCC`
- MUST have at least 0.1" gap below the title text

### McKinsey Footer (REQUIRED — Auto-Checked)
- Source line at y=6.6": "Source: [description]; McKinsey analysis" — 8pt, grey, left-aligned
- Footer divider line at y=6.9": thin grey line spanning full width
- Footer text at y=7.0": "CONFIDENTIAL" (left) and page number (right) — 8pt, grey
- **All three footer components are MANDATORY**

### Structured Data Table
- When any structured data is present, it MUST be rendered as a proper table
- Table header: light grey fill (`#F2F2F2`), navy bold text
- Gridlines: `#D9D9D9`, 0.75pt
- Data cells: white fill, dark grey text, 10–11pt
- See LAYOUT_PATTERNS.md for full specification

## Layout Rules
- **Margins**: 0.5" on all sides minimum
- **Body content zone**: y=1.4" to y=6.5" (hard limits — content must not exceed these bounds)
- **Content spacing**: minimum 0.15" between any two elements
- **Alignment**: All elements must snap to a consistent grid; left-align text by default
- **Boxes**: Thin borders (0.75pt) in light grey. NO fill or very light grey fill (#F5F5F5). NEVER solid colored fills.
- **Lines**: Always thin (0.5–1pt). Never thick or heavy.
- **Icons**: Do NOT place icons overlapping text. Either put icons in their own separate space with 0.2" padding from text, or omit icons entirely (preferred).

## Content Structure (Top to Bottom — Fixed Positions)
1. **Title area** (y=0.4"–1.1"): Insight title, 18–22pt Georgia bold navy
2. **Divider line** (y=1.2"): Thin grey horizontal rule
3. **Body content** (y=1.4"–6.5"): Charts, tables, diagrams — clean and minimal
4. **Source line** (y=6.6"): "Source: ..." — 8pt grey, left-aligned
5. **Footer line** (y=6.9"): Thin grey horizontal rule
6. **Footer area** (y=7.0"): CONFIDENTIAL (left) + page number (right)

## What to AVOID
- ❌ **Truncated text** — the #1 most damaging error. NEVER allow text to be cut off
- ❌ **Overlapping elements** — title over divider, icons over text, source over content
- ❌ **Missing footer** — "CONFIDENTIAL" and page number are mandatory
- ❌ **Missing data table** — structured data must use a proper table, not free-floating text
- ❌ **Title font too large** — use 18–22pt, not 24–28pt
- ❌ Dark or colored backgrounds
- ❌ Solid-filled boxes or shapes with saturated colors
- ❌ Thick borders or lines (anything > 1.5pt)
- ❌ Generic topic-label titles (e.g., "Market Overview", "Strategy Update")
- ❌ Centered source text — always left-align
- ❌ Bright or vibrant accent colors (teal, cyan, green, orange)
- ❌ Content extending below y=6.5" (into source/footer zone)
