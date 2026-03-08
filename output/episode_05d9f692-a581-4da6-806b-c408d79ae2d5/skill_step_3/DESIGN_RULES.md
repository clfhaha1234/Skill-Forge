# McKinsey-Style Slide Design Rules

## ⚠️ TOP 4 CRITICAL RULES (Most Common Failures)
1. **NO TEXT TRUNCATION** — Every text string must be fully visible. Never let text get cut off (e.g., "National Hydrog..." is UNACCEPTABLE). Size containers to fit text, reduce font size, or use shorter labels. See TEXT_FITTING_RULES.md.
2. **NO OVERLAPPING ELEMENTS** — Title must not overlap divider. Icons must not overlap text. Source must not overlap content. Footer must not overlap source. Every element needs clear spacing. See LAYOUT_PATTERNS.md.
3. **STRUCTURED DATA TABLE WITH McKINSEY BORDERS** — When presenting data, use a proper table with McKinsey-style borders (thick 2pt navy header border, minimal 0.5pt internal gridlines, no heavy outer box). Free-floating text boxes for data = FAIL. See TABLE_STYLING.md for detailed implementation.
4. **McKINSEY & COMPANY FOOTER BRANDING** — Every slide MUST include "McKinsey & Company" text in the bottom-right footer area alongside the page number. Missing this = automatic Patronus FAIL. See FOOTER_AND_STRUCTURE.md.

## CRITICAL DESIGN PRINCIPLES
1. **White background** — ALWAYS use a clean white (`FFFFFF`) background. Never use dark backgrounds.
2. **Insight-driven title** — The title must be a "so-what" statement, NOT a topic label. Keep it under 120 characters so it fits in 1–2 lines at 18–22pt.
3. **Minimalist, restrained design** — Less is more. Avoid heavy graphics, thick borders, and solid-filled boxes. Use white space generously.
4. **Professional polish** — Every element must be precisely aligned, consistently spaced, and purposefully placed. Zero overlaps, zero truncation. Attention to detail in borders, spacing, and alignment distinguishes professional from generic output.
5. **Proper McKinsey footer** — Every slide MUST have: source attribution (anchored near bottom at y=6.75"), footer divider line, "CONFIDENTIAL" (left), **"McKinsey & Company"** + page number (right). This is auto-checked.

## Color Palette (MANDATORY — McKinsey Brand)
- **Primary text**: Dark navy `#003A70` or near-black `#1A1A2E`
- **Secondary text / labels**: Medium grey `#666666` or `#58595B`
- **Accent (sparingly)**: McKinsey blue `#0072CE` — used only for key highlights
- **Backgrounds**: Pure white `#FFFFFF` only
- **Borders / lines**: Light grey `#CCCCCC` or `#D9D9D9`
- **Table header fill**: Very light grey `#F2F2F2`
- **Table header bottom border**: **Navy `#003A70`, 2pt** — signature McKinsey table style
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
- **Source / footnote text**: Calibri or Arial, 8pt, regular, medium grey `#666666`
- **Numbers / data**: Calibri or Arial, can be bold for emphasis

## Mandatory Structural Elements

### Thin Divider Line Under Title
- Position: y=1.2", from x=0.5" to x=9.5"
- Style: 0.75–1pt weight, light grey `#CCCCCC`
- MUST have at least 0.1" gap below the title text

### McKinsey Footer (REQUIRED — Auto-Checked)
- Source line at **y=6.75"**: "Source: [description]; McKinsey analysis" — 8pt, grey, left-aligned
  - ⚠️ Source must be anchored **close to the bottom edge**, not floating high in the middle
- Footer divider line at y=6.9": thin grey line spanning full width
- Footer text at y=7.0": "CONFIDENTIAL" (left) and **"McKinsey & Company"** + page number (right) — 8pt, grey
- **All four footer components are MANDATORY**: source, divider, confidential text, McKinsey & Company branding + page number

### Structured Data Table (McKinsey Border Style)
- When any structured data is present, it MUST be rendered as a proper table
- **Table header**: light grey fill (`#F2F2F2`), navy bold text, **2pt navy bottom border** ← SIGNATURE ELEMENT
- **Internal gridlines**: 0.5pt, light grey `#D9D9D9` — horizontal only preferred, minimal
- **No heavy outer box border** — table should float cleanly on white background
- **Bottom border of table**: 1pt navy for clean closure
- Data cells: white fill, dark grey text, 10–11pt
- See **TABLE_STYLING.md** for detailed border hierarchy and Python-PPTX code examples

## Layout Rules
- **Margins**: 0.5" on all sides minimum
- **Body content zone**: y=1.4" to y=6.4" (hard limits — content must not exceed these bounds)
- **Source zone**: y=6.75" (anchored close to footer, not floating high)
- **Content spacing**: minimum 0.15" between any two elements
- **Alignment**: All elements must snap to a consistent grid; left-align text by default
- **Boxes**: Thin borders (0.75pt) in light grey. NO fill or very light grey fill (#F5F5F5). NEVER solid colored fills.
- **Lines**: Always thin (0.5–1pt). Never thick or heavy. Exception: table header bottom border (2pt navy).
- **Icons**: Do NOT place icons overlapping text. Either put icons in their own separate space with 0.2" padding from text, or omit icons entirely (preferred).

## Content Structure (Top to Bottom — Fixed Positions)
1. **Title area** (y=0.4"–1.1"): Insight title, 18–22pt Georgia bold navy
2. **Divider line** (y=1.2"): Thin grey horizontal rule
3. **Body content** (y=1.4"–6.4"): Charts, tables, diagrams — clean and minimal
4. **Source line** (y=6.75"): "Source: ..." — 8pt grey, left-aligned, **anchored near bottom**
5. **Footer line** (y=6.9"): Thin grey horizontal rule
6. **Footer area** (y=7.0"): CONFIDENTIAL (left) + **McKinsey & Company** + page number (right)

## Professional Polish Checklist
These details separate a professional McKinsey slide from a generic one:
- [ ] Table header has a **thick navy bottom border** (2pt) — not generic uniform gridlines
- [ ] Table internal gridlines are **subtle and minimal** (0.5pt light grey, horizontal only)
- [ ] No vertical gridlines in table (preferred) — cleaner horizontal-only separators
- [ ] Table has **no heavy outer box border** — floats on white background
- [ ] Table bottom row has a **1pt navy closing border**
- [ ] Source text is **anchored near the bottom** (y=6.75"), not floating high
- [ ] Footer includes **"McKinsey & Company"** branding in bottom-right
- [ ] All text elements have consistent font families (Georgia for title, Calibri/Arial for body)
- [ ] Numbers in tables are right-aligned; text is left-aligned
- [ ] No unnecessary visual clutter — every element serves a purpose
- [ ] Consistent spacing between all elements (no irregular gaps)
- [ ] Overall impression: clean, authoritative, and unmistakably professional

## What to AVOID
- ❌ **Truncated text** — the #1 most damaging error. NEVER allow text to be cut off
- ❌ **Overlapping elements** — title over divider, icons over text, source over content
- ❌ **Missing footer branding** — "McKinsey & Company" in bottom-right is MANDATORY
- ❌ **Missing data table** — structured data must use a proper table, not free-floating text
- ❌ **Generic table borders** — uniform-weight gridlines look like Excel, not McKinsey. Use thick navy header border + thin grey internals. See TABLE_STYLING.md.
- ❌ **Source text floating high** — source must anchor near bottom (y=6.75"), not mid-slide
- ❌ **Title font too large** — use 18–22pt, not 24–28pt
- ❌ Dark or colored backgrounds
- ❌ Solid-filled boxes or shapes with saturated colors
- ❌ Thick borders or lines (anything > 1.5pt) — except table header border which is 2pt navy
- ❌ Generic topic-label titles (e.g., "Market Overview", "Strategy Update")
- ❌ Centered source text — always left-align
- ❌ Bright or vibrant accent colors (teal, cyan, green, orange)
- ❌ Content extending below y=6.4" (into source/footer zone)
