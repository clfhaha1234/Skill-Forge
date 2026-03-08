# Layout Rules — Precise Spatial Guidelines

This file defines exact positioning to prevent layout errors like overlapping elements.

---

## Slide Dimensions
- Standard: 13.333" × 7.5" (widescreen 16:9)

## Vertical Zones (Top to Bottom)

```
┌─────────────────────────────────────────┐  0.0"
│  Top margin (empty)                      │  0.0" – 0.4"
├─────────────────────────────────────────┤  0.4"
│  TITLE ZONE                              │  0.4" – 1.1"
│  - Title text: top=0.4", left=0.5"       │
│  - Font: Georgia, 22-26pt, Bold, White   │
│  - Max height: ~0.7" (1-2 lines)         │
├─────────────────────────────────────────┤  1.1"
│  DIVIDER LINE                            │  1.1" – 1.15"
│  - Thin horizontal line (#4A90D9, 1pt)   │
│  - left=0.5", width=12.333"             │
├─────────────────────────────────────────┤  1.15"
│  GAP (breathing room)                    │  1.15" – 1.4"
├─────────────────────────────────────────┤  1.4"
│                                          │
│  CONTENT ZONE                            │  1.4" – 6.3"
│  - Tables, charts, text blocks           │
│  - All content MUST start at or below    │
│    1.4" from top                         │
│  - All content MUST END by 6.3" from top │
│                                          │
├─────────────────────────────────────────┤  6.3"
│  BUFFER (empty breathing room)           │  6.3" – 6.5"
│  - NO content, NO source text here       │
│  - Ensures separation between content    │
│    and source note                        │
├─────────────────────────────────────────┤  6.5"
│  SOURCE NOTE                             │  6.5" – 6.8"
│  - Small italic text, left-aligned       │
│  - Calibri 8-9pt, #8899AA               │
│  - MUST NOT overlap with any content     │
├─────────────────────────────────────────┤  6.8"
│  GAP                                     │  6.8" – 7.0"
├─────────────────────────────────────────┤  7.0"
│  FOOTER                                  │  7.0" – 7.5"
│  - "McKinsey & Company  |  [#]"          │
│  - Right-aligned, Calibri 9pt, #8899AA   │
└─────────────────────────────────────────┘  7.5"
```

## ⚠️ CRITICAL: Bottom Margin & Overlap Prevention

The #1 layout error is content (especially tables) running too far down the slide and overlapping with the source note or footer. To prevent this:

1. **Content MUST end by 6.3"** — this is a hard limit, not a suggestion
2. **Source note starts at 6.5"** — there is a 0.2" buffer between content and source
3. **Footer starts at 7.0"** — there is a 0.2" buffer between source and footer
4. If content won't fit, **reduce font size, reduce rows, or split to another slide** — NEVER extend past 6.3"
5. **Always verify** that the bottom edge of your last content element is above 6.3"

## Horizontal Zones

```
│0.5"│◄─────────── Content Area: 12.333" ──────────────►│0.5"│
     │                                                    │
     No vertical        Content spans                  No vertical
     sidebar text       full width or                  sidebar text
                        in 2-3 columns
```

## CRITICAL RULES

1. **No element may be placed above 1.4" from top EXCEPT the title and divider**
2. **No content element may overlap the title zone (0.4"–1.1")**
3. **No content element may extend below 6.3" from top**
4. **No source text may overlap with any content element**
5. **No vertical text sidebars on left or right edges**
6. **Content boxes must have explicit top position ≥ 1.4"**
7. **If content is too tall, reduce font size or split across slides — never extend past limits**

## Table Sizing Guidelines

For a full-width table in the content zone:
- **Top: 1.4"**
- **Left: 0.5"**
- **Width: 12.333"**
- **Max height: 4.9"** (from 1.4" to 6.3" = 4.9" available)
- Use generous row heights (~0.4"-0.5" per row) so tables feel open and airy
- For a table with 5 rows (header + 4 data): ~0.5" per row = 2.5" total, ending at 3.9" — well within limits

### Row Height Calculation:
- Header row: 0.45"
- Data rows: 0.4" each
- For N data rows: total height = 0.45" + (N × 0.4")
- **Max data rows for full-width table: ~11 rows** (but prefer fewer for readability)
- **Preferred: 3-6 data rows** for clean, spacious appearance

For a 3-column layout:
- Column width: ~3.8" each
- Gap between columns: 0.35"
- All three columns start at top: 1.4"
- All three columns end by: 6.3"

## Z-Order
- Title: always on top (highest z-order)
- Divider line: just below title
- Content elements: below divider
- Background: lowest z-order
- Never place any shape that could obscure the title

## Background Color Enforcement
- The slide background MUST be `#002244` (dark navy)
- **NEVER use white (`#FFFFFF`) as a slide background**
- **NEVER use any light color as a slide background**
- Set the slide background explicitly to `#002244` as the very first step
