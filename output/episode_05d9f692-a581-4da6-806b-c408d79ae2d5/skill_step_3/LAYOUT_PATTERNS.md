# Layout Patterns — Precise Positioning & Data Tables

## Slide Coordinate System
- Standard slide dimensions: **10" wide × 7.5" tall**
- Usable area after 0.5" margins: **9" wide × 6.5" tall** (from 0.5",0.5" to 9.5",7.0")
- However, the bottom 1.1" is reserved for source + footer

## Precise Vertical Zone Map

| Zone | Y-Start | Y-End | Height | Contents |
|------|---------|-------|--------|----------|
| Title | 0.4" | 1.1" | 0.7" | Insight title (18–22pt, 1–2 lines max) |
| Divider | 1.2" | 1.2" | line | Thin grey horizontal rule |
| Body | 1.4" | 6.4" | 5.0" | Main content area |
| Source | 6.75" | 6.85" | 0.1" | Source attribution text (anchored near bottom) |
| Footer line | 6.9" | 6.9" | line | Thin grey horizontal rule |
| Footer | 7.0" | 7.2" | 0.2" | CONFIDENTIAL (left) + McKinsey & Company + page # (right) |

**CRITICAL**: Body content MUST stay within 1.4" to 6.4" vertically. Source text anchors at y=6.75", close to the footer divider line. Never let content bleed into the source/footer zone.

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
┌──────────┐  ┌──────────┐  ┌──────────┐           y: 4.0"–6.2"
│  Metric 1 │  │  Metric 2 │  │  Metric 3 │
│  €XX B    │  │  XX GW    │  │  XX,000   │
│  detail   │  │  detail   │  │  jobs     │
└──────────┘  └──────────┘  └──────────┘
                                                     y: 6.4" (STOP - no content below here)
Source: ...                                          y: 6.75"
─────────────────────────────────────────────        y: 6.9"
CONFIDENTIAL                 McKinsey & Company  1   y: 7.0"
```

**CRITICAL**: The bottom metric boxes must end by y = 6.2" to leave room for source and footer with clear separation.

## Structured Data Table Pattern — MANDATORY

### When to Use a Data Table
- Whenever the slide contains structured/comparative data
- Whenever there are multiple data points that can be organized in rows/columns
- Use a table INSTEAD of free-floating text boxes for data

### ⚠️ Table Border Styling — McKinsey Reference Style (CRITICAL)
McKinsey tables do NOT use uniform generic gridlines. They follow a specific hierarchy:

#### Header Border Treatment:
- **Bottom border of header row**: **2pt solid navy `#003A70`** — this is the MOST IMPORTANT border
- **Top border of header row**: 1pt solid navy `#003A70`
- This thick navy line below the header row is a signature McKinsey table element

#### Internal Gridline Treatment:
- **Horizontal internal gridlines** (between data rows): 0.5pt, light grey `#D9D9D9` — thin and subtle
- **Vertical internal gridlines**: 0.5pt, light grey `#D9D9D9` — or OMIT entirely for cleaner look
- McKinsey style prefers **minimal internal gridlines** — just enough to guide the eye
- For cleaner tables, use only horizontal row separators (no vertical lines between data cells)

#### Outer Border Treatment:
- **No heavy outer border** — the table should "float" on the white background
- Bottom border of last row: 1pt, `#003A70` navy or `#999999` grey
- Left and right outer borders: NONE or 0.5pt light grey — keep minimal

### Table Construction Rules
- **Position**: centered in the body area, with 0.3" padding from edges
- **Column widths**: distribute evenly, or size proportionally to content
- **Row height**: minimum 0.35" per row to prevent text clipping
- **Header row**: light grey fill (`#F2F2F2`), navy bold text (`#003A70`), 11pt
  - **Thick 2pt navy bottom border** on header row (signature McKinsey style)
- **Data cells**: white fill, dark grey text (`#333333`), 10–11pt
- **Internal gridlines**: thin 0.5pt, light grey `#D9D9D9` — horizontal only preferred
- **Cell padding**: at least 0.05" on all sides (text must not touch cell edges)
- **Text alignment**: Left-align text, right-align numbers
- **Alternating row shading** (optional): very subtle `#F9F9F9` on even rows for readability

### ❌ WRONG Table Borders (Generic):
```
┌─────────────────┬──────────┬──────────┬──────────┐  ← All borders same weight
│ Category        │ 2025     │ 2030     │ 2035     │     and same color
├─────────────────┼──────────┼──────────┼──────────┤  ← Looks like a spreadsheet
│ Capacity        │ 1 GW     │ 5 GW     │ 10 GW   │
├─────────────────┼──────────┼──────────┼──────────┤
│ Investment      │ €2B      │ €8B      │ €15B     │
└─────────────────┴──────────┴──────────┴──────────┘
```

### ✅ CORRECT Table Borders (McKinsey Style):
```
  Category          2025       2030       2035        ← Header: #F2F2F2 bg, navy bold
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 2pt navy border under header
  Capacity          1 GW       5 GW       10 GW      ← White bg, grey text
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ← 0.5pt light grey (subtle)
  Investment        €2B        €8B        €15B
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ← 0.5pt light grey (subtle)
  Jobs created      3,000      8,000      15,000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 1pt navy bottom border
```

Key differences from generic tables:
1. **Thick navy line under header** (2pt) — most distinctive feature
2. **Minimal/thin internal gridlines** (0.5pt light grey) — not prominent
3. **No heavy outer box border** — clean and open
4. **Optional: no vertical gridlines** — cleaner horizontal-only separators
5. **Navy bottom border** (1pt) — provides clean closure

### Python-PPTX Table Border Implementation
```python
# For header row bottom border (thick navy):
from pptx.oxml.ns import qn
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor

# Set thick navy bottom border on header cells:
for cell in header_row_cells:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # Bottom border: 2pt navy
    bottom = OxmlElement('a:lnB')
    bottom.set('w', str(Emu(Pt(2))))  # 2pt width
    solidFill = OxmlElement('a:solidFill')
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '003A70')
    solidFill.append(srgbClr)
    bottom.append(solidFill)
    tcPr.append(bottom)

# For data row internal borders (thin grey):
for cell in data_cells:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # Bottom border: 0.5pt light grey
    bottom = OxmlElement('a:lnB')
    bottom.set('w', str(Emu(Pt(0.5))))
    solidFill = OxmlElement('a:solidFill')
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', 'D9D9D9')
    solidFill.append(srgbClr)
    bottom.append(solidFill)
    tcPr.append(bottom)
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
4. **Footer line must be at least 0.05" below source text**
5. **Title must end at least 0.1" above the divider line**
6. If elements would overlap, REDUCE content, SHRINK font sizes, or RESTRUCTURE layout — NEVER allow overlap
