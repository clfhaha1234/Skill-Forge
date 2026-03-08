# Layout Patterns — Precise Positioning & Data Tables

## Slide Coordinate System
- Standard slide dimensions: **10" wide × 7.5" tall**
- Usable area after 0.5" margins: **9" wide × 6.5" tall** (from 0.5",0.5" to 9.5",7.0")
- However, the bottom 0.8" is reserved for source + footer

## Precise Vertical Zone Map

| Zone | Y-Start | Y-End | Height | Contents |
|------|---------|-------|--------|----------|
| Title | 0.4" | 1.1" | 0.7" | Insight title (18–22pt, 1–2 lines max) |
| Divider | 1.2" | 1.2" | line | Thin grey horizontal rule |
| Body | 1.4" | 6.5" | 5.1" | Main content area |
| Source | 6.6" | 6.8" | 0.2" | Source attribution text |
| Footer line | 6.9" | 6.9" | line | Thin grey horizontal rule |
| Footer | 7.0" | 7.2" | 0.2" | CONFIDENTIAL (left) + page # (right) |

**CRITICAL**: Body content MUST stay within 1.4" to 6.5" vertically. Never let content bleed into the source/footer zone.

## Timeline/Process Flow Layout Pattern

### Horizontal Timeline (≤ 4 phases)
When there are 4 or fewer phases, use a single horizontal row:

```
|  Phase 1       |  Phase 2       |  Phase 3       |  Phase 4       |
|  (2.0" wide)   |  (2.0" wide)   |  (2.0" wide)   |  (2.0" wide)   |
```
- Box width: `(9.0 - (N-1) × 0.25) / N` inches each (with 0.25" gaps)
- Box height: 0.7–1.0"
- Font inside boxes: 10–11pt
- Short label on line 1 (bold), description on line 2–3 (regular, 9pt)

### Horizontal Timeline (5–7 phases)
When 5–7 phases, boxes get narrow. Use these adaptations:
- Font size: **9pt** for labels
- Use abbreviated/short text (2–4 words max per line)
- Box width: minimum 1.2", reduce gaps to 0.15"
- Put detailed descriptions in a separate row BELOW the timeline boxes
- Or use a **two-row stacked layout**

### Vertical/List Timeline (> 7 phases or long descriptions)
Switch to a vertical list format:
```
2024  ●——  Phase 1: Short label
           Full description text here (up to 2 lines)

2026  ●——  Phase 2: Short label  
           Full description text here

2030  ●——  Phase 3: Short label
           Full description text here
```
- This avoids ALL horizontal space constraints
- Each entry gets the full 9" width for text

### Timeline with Summary Metrics Below
A common McKinsey pattern: timeline on top, key metrics/callouts on bottom.

```
┌────────────────────────────────────────────────┐  y: 1.4"–3.5"
│           TIMELINE / PROCESS FLOW               │
│  [Phase boxes with short labels]                │
└────────────────────────────────────────────────┘
                                                     y: 3.7"–4.0" (subheading)
┌──────────┐  ┌──────────┐  ┌──────────┐           y: 4.0"–6.3"
│  Metric 1 │  │  Metric 2 │  │  Metric 3 │
│  €XX B    │  │  XX GW    │  │  XX,000   │
│  detail   │  │  detail   │  │  jobs     │
└──────────┘  └──────────┘  └──────────┘
                                                     y: 6.5" (STOP - no content below here)
Source: ...                                          y: 6.6"
─────────────────────────────────────────────        y: 6.9"
CONFIDENTIAL                                    1    y: 7.0"
```

**CRITICAL**: The bottom metric boxes must end by y = 6.3" to leave room for source and footer with clear separation.

## Structured Data Table Pattern — MANDATORY

### When to Use a Data Table
- Whenever the slide contains structured/comparative data
- Whenever there are multiple data points that can be organized in rows/columns
- Use a table INSTEAD of free-floating text boxes for data

### Table Construction Rules
- **Position**: centered in the body area, with 0.3" padding from edges
- **Column widths**: distribute evenly, or size proportionally to content
- **Row height**: minimum 0.35" per row to prevent text clipping
- **Header row**: light grey fill (`#F2F2F2`), navy bold text (`#003A70`), 11pt
- **Data cells**: white fill, dark grey text (`#333333`), 10–11pt
- **Gridlines**: thin grey (`#D9D9D9`), 0.75pt — all internal gridlines
- **No outer border** or very thin outer border (0.5pt, `#D9D9D9`)
- **Cell padding**: at least 0.05" on all sides (text must not touch cell edges)
- **Text alignment**: Left-align text, right-align numbers

### Example Table Structure
```
┌─────────────────┬──────────┬──────────┬──────────┐
│ Category        │ 2025     │ 2030     │ 2035     │  ← Header row (#F2F2F2 bg)
├─────────────────┼──────────┼──────────┼──────────┤
│ Electrolyzer    │ 1 GW     │ 5 GW     │ 10 GW   │  ← White bg, grey text
│ capacity        │          │          │          │
├─────────────────┼──────────┼──────────┼──────────┤
│ Investment      │ €2B      │ €8B      │ €15B     │
│ required        │          │          │          │
├─────────────────┼──────────┼──────────┼──────────┤
│ Jobs created    │ 3,000    │ 8,000    │ 15,000   │
└─────────────────┴──────────┴──────────┴──────────┘
```

## Content Density Guidelines
- **Maximum elements per slide**: 6–8 distinct content blocks
- If a timeline has more than 5 phases, simplify to 3–4 key phases and add a "detail" note
- If bottom metrics exceed 3–4 items, use a table instead of separate boxes
- White space is a FEATURE, not wasted space — at least 30% of body area should be whitespace

## Anti-Overlap Rules (MANDATORY)
1. **No element may overlap another element** — verify all bounding boxes are non-intersecting
2. **Minimum gap between any two elements**: 0.15" (vertical) or 0.2" (horizontal)
3. **Source text must be at least 0.15" below the lowest body content element**
4. **Footer line must be at least 0.1" below source text**
5. **Title must end at least 0.1" above the divider line**
6. If elements would overlap, REDUCE content, SHRINK font sizes, or RESTRUCTURE layout — NEVER allow overlap
