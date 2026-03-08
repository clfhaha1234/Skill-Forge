# Design Rules — McKinsey-Style Consulting Slides

## CRITICAL: Slide Background
- Background MUST be **WHITE** (`FFFFFF`). Never use dark/black backgrounds.
- All slides use a clean, white canvas. This is non-negotiable.

## Color Palette — Muted Professional Tones
Use a restrained, conservative palette inspired by top-tier consulting firms:
- **Primary text**: `333333` (dark charcoal) — all body text
- **Title text**: `333333` (dark charcoal) — titles use serif font (see Typography)
- **Secondary text**: `666666` (medium gray) — subtitles, labels, captions
- **Accent / highlight**: `003A70` (deep navy blue) — section headers, key callouts, table headers
- **Accent secondary**: `4472C4` (muted steel blue) — chart bars, table accents, subtle highlights
- **Accent tertiary**: `D6DCE4` (light cool gray) — table row shading, background fills, divider lines
- **Border / lines**: `A6A6A6` (medium gray) — table borders, divider rules
- **AVOID**: Bright teal, seafoam, mint, neon colors, saturated greens. Keep everything muted and professional.
- Use at most 3 colors on any single slide (excluding black/white/gray).

## Typography

### CRITICAL: Title Font — SERIF
- **Title**: **Georgia** (serif font), **22–26pt**, bold, color `333333`
  - The title MUST use a **serif font (Georgia)**. This is the distinctive McKinsey style.
  - DO NOT use Arial or Calibri for the title. Titles are ALWAYS in Georgia (serif).
  - Titles must be **insight-driven "so-what" statements** — not topic labels.
  - GOOD: "Hydrogen production costs have fallen 40% since 2015, driven by electrolyzer scale-up"
  - BAD: "Hydrogen Market Overview" or "Industry Trends"
  - The title is the #1 takeaway the audience should remember from this slide.

### Body and Other Text — SANS-SERIF
- **Subtitle** (optional): Arial or Calibri, 14–16pt, regular, color `666666`
- **Body text**: Arial or Calibri, 12–14pt, regular, color `333333`
  - Minimum body text size: **12pt**. Never go below 12pt for any readable content.
- **Table text**: Arial or Calibri, 10–12pt, color `333333`
  - Minimum table text size: **10pt**. Never go below 10pt.
- **Footer text**: Arial or Calibri, 8–9pt, color `999999`

### Font Summary Table
| Element | Font | Style | Size | Color |
|---------|------|-------|------|-------|
| Title | **Georgia** (serif) | Bold | 22–26pt | `333333` |
| Subtitle | Arial/Calibri | Regular | 14–16pt | `666666` |
| Body text | Arial/Calibri | Regular | 12–14pt | `333333` |
| Table text | Arial/Calibri | Regular | 10–12pt | `333333` |
| Footer | Arial/Calibri | Italic (source) / Regular (page) | 8–9pt | `999999` |

## Title Area & Divider Line
- Title sits at the top of the slide within the safe margin area.
- Title text is LEFT-ALIGNED.
- Title font is **Georgia** (serif), bold — this creates the distinctive consulting look.
- Immediately below the title, draw a **horizontal divider line** spanning the content width:
  - Color: `003A70` (deep navy) or `A6A6A6` (gray)
  - Weight: 1.0–1.5pt
  - Position: ~0.15" below the title text baseline
- This divider line is REQUIRED on every slide. It visually separates the title from body content.

## Layout & Margins
- **Margins**: 0.75" left, 0.75" right, 0.6" top (to start of title), 0.7" bottom (reserved for footer)
- **Content area**: Everything between the divider line and the footer zone
- **Spacing**: 0.3–0.5" gap between major content blocks
- **OVERLAP PREVENTION**: 
  - Calculate exact positions for every element. Never let text boxes overlap.
  - Title zone: top 0.6" to ~1.3" (title + divider)
  - Content zone: ~1.4" to ~6.6" (main body)
  - Footer zone: 6.7" to 7.2" (bottom strip)
  - Ensure text boxes have adequate width — never let text wrap into overlapping adjacent elements.
  - Test: Every element's bounding box must not intersect any other element's bounding box.

## Structured Data Tables — CLEAN OPEN STYLE
When presenting data, comparisons, or multi-item information, use a **structured table** with a clean, open design:

### Table Style Rules (CRITICAL — No Heavy Grid Lines)
- **DO NOT use full grid/box borders** around every cell. This looks heavy and dated.
- Use a **clean, open table style** with primarily **horizontal lines** and **background fills**:
  - **Header row**: fill `003A70` (navy), text white `FFFFFF`, bold, 11–12pt
  - **Header bottom border**: 1.5pt solid white or navy — separates header from body
  - **Body rows**: Alternating white `FFFFFF` and light gray `F2F2F2` fills
  - **Horizontal lines only**: Thin horizontal rules (`D6DCE4`, 0.5pt) between body rows, OR rely solely on alternating row fills for separation (no lines at all between rows)
  - **NO vertical lines** between columns. Column separation comes from cell padding and white space.
  - **Bottom border**: Optional thin line (`D6DCE4`, 0.5pt) under the last row
  - **NO left/right outer borders** on the table
- Cell padding: generous — at least 0.08" on all sides to prevent text from touching edges
- Column widths: proportional to content; ensure no text truncation
- Tables should be horizontally centered in the content area
- Prefer tables over timelines, process flows, or freeform layouts for data presentation

### Table Border Summary
| Border Type | Use? | Details |
|-------------|------|---------|
| Full grid (all cells) | **NO** | Never use full grid borders |
| Vertical lines | **NO** | No vertical column separators |
| Header bottom edge | YES | 1.5pt, white or navy |
| Horizontal row separators | OPTIONAL | 0.5pt `D6DCE4` — or use row fills only |
| Outer left/right borders | **NO** | Leave open |
| Bottom table border | OPTIONAL | 0.5pt `D6DCE4` |

## Footer — McKinsey Standard Format
Every slide MUST have a footer strip at the bottom containing:
- **Left side**: Source attribution (e.g., "Source: IEA World Energy Outlook 2023; McKinsey analysis")
  - Font: 8–9pt, color `999999`, italic
- **Right side**: **"McKinsey & Company"** followed by the page number, separated by a pipe or spaces
  - Format: "McKinsey & Company  |  1" OR place "McKinsey & Company" text with page number to its right
  - Alternatively: "McKinsey & Company" as separate text element next to the page number
  - Font: 8–9pt, color `999999`
  - The **"McKinsey & Company"** branding text is MANDATORY in the footer — never omit it.
- **Separator**: A thin horizontal line (`D6DCE4`, 0.5pt) at the top of the footer zone (~Y=6.55") spanning the content width
- Footer elements must sit BELOW this line, within the 6.7"–7.1" vertical zone
- The footer must NEVER overlap with body content above it

## Professional Polish Checklist
Before finalizing any slide, verify:
1. ☐ Background is white
2. ☐ Title is an insight-driven statement (not a topic label)
3. ☐ **Title uses Georgia (serif font), bold** — NOT Arial/Calibri
4. ☐ Title divider line is present
5. ☐ No text overlapping anywhere
6. ☐ All text is readable (minimum sizes respected)
7. ☐ Color palette is restrained (navy, gray, white — no bright colors)
8. ☐ Data is presented in a structured table (if applicable)
9. ☐ **Table uses clean open style** — horizontal lines and fills only, NO full grid, NO vertical lines
10. ☐ Footer with source and page number is present
11. ☐ **"McKinsey & Company" branding appears in bottom-right footer**
12. ☐ Margins are respected — no elements within 0.5" of slide edges
13. ☐ Overall look is clean, sparse, and authoritative
