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
│  - Max height: ~0.7" (1-2 lines)         │
├─────────────────────────────────────────┤  1.1"
│  DIVIDER LINE                            │  1.1" – 1.15"
│  - Thin horizontal line (#4A90D9, 1pt)   │
│  - left=0.5", width=12.333"             │
├─────────────────────────────────────────┤  1.15"
│  GAP (breathing room)                    │  1.15" – 1.4"
├─────────────────────────────────────────┤  1.4"
│                                          │
│  CONTENT ZONE                            │  1.4" – 6.7"
│  - Tables, charts, text blocks           │
│  - All content MUST start at or below    │
│    1.4" from top                         │
│                                          │
├─────────────────────────────────────────┤  6.7"
│  SOURCE NOTE                             │  6.7" – 7.0"
│  - Small italic text, left-aligned       │
├─────────────────────────────────────────┤  7.0"
│  FOOTER                                  │  7.0" – 7.5"
│  - "McKinsey & Company  |  [#]"          │
│  - Right-aligned, 9pt, muted             │
└─────────────────────────────────────────┘  7.5"
```

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
3. **No vertical text sidebars on left or right edges**
4. **Content boxes must have explicit top position ≥ 1.4"**
5. **If content is too tall, reduce font size or split across slides — never push into title zone**

## Table Sizing Guidelines

For a full-width table in the content zone:
- Top: 1.4"
- Left: 0.5"
- Width: 12.333"
- Max height: 5.3" (to leave room for source + footer)

For a 3-column layout:
- Column width: ~3.8" each
- Gap between columns: 0.35"
- All three columns start at top: 1.4"

## Z-Order
- Title: always on top (highest z-order)
- Divider line: just below title
- Content elements: below divider
- Background: lowest z-order
- Never place any shape that could obscure the title
