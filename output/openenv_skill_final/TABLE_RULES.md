# Table Rules — Clean Open Table Design

## CRITICAL: No Heavy Grid Lines
The biggest mistake in table design is using full grid borders (lines around every cell).
This looks heavy, cluttered, and dated. McKinsey-style tables use a **clean, open design**
with minimal lines and background fills for visual separation.

## The Clean Open Table Style

### What TO Do ✓
- Use **horizontal lines only** (or no lines at all, relying on row fills)
- Use **alternating row background fills** for visual grouping
- Use **generous cell padding** for breathing room
- Leave column separation to **white space** — no vertical dividers
- Keep the overall look **light and airy**

### What NOT To Do ✗
- **NO full grid borders** (lines around every cell)
- **NO vertical lines** between columns
- **NO heavy outer border** framing the entire table
- **NO thick borders** (keep all lines ≤ 1pt except header bottom at 1.5pt)
- **NO dark borders on body rows** — use `D6DCE4` light gray if using any lines

## Table Structure

### Header Row
- Background fill: `003A70` (navy)
- Text: White `FFFFFF`, bold, 11–12pt, Arial/Calibri
- Bottom edge: 1.5pt solid (can be white gap or navy; creates clean separation from body)
- No top border, no left/right borders

### Body Rows
- **Alternating fills**: Row 1 = `FFFFFF` (white), Row 2 = `F2F2F2` (light gray), alternating
- Text: `333333`, regular, 10–12pt, Arial/Calibri
- **Row separation**: Use the alternating fills as the primary separator. If additional clarity is needed, add very thin horizontal lines (`D6DCE4`, 0.5pt) between rows.
- **NO vertical lines** — columns are separated by cell padding/white space only
- **NO left or right borders** on the table

### Bottom Edge
- Optional: thin bottom border under the last row, `D6DCE4`, 0.5pt
- Or leave open (no bottom border)

## Border Specification Summary

```
Table outer borders:     NONE (no top, left, right, bottom frame)
Vertical cell borders:   NONE (no column separators)
Header bottom border:    1.5pt, white or navy
Body row separators:     0.5pt, #D6DCE4 (optional — row fills can suffice)
Bottom table border:     0.5pt, #D6DCE4 (optional)
```

## Visual Example (ASCII Representation)

```
┌──────────────────────────────────────────────────────────┐
│  [Navy fill #003A70]                                      │
│  Column A        Column B        Column C        Column D │  ← White bold text
│──────────────────────────────────────────────────────────│  ← 1.5pt separator
│  Data 1a         Data 1b         Data 1c         Data 1d │  ← White row
│  · · · · · · · · · · · · · · · · · · · · · · · · · · · ·│  ← Optional thin line
│  Data 2a         Data 2b         Data 2c         Data 2d │  ← #F2F2F2 gray row
│  · · · · · · · · · · · · · · · · · · · · · · · · · · · ·│  ← Optional thin line
│  Data 3a         Data 3b         Data 3c         Data 3d │  ← White row
└──────────────────────────────────────────────────────────┘
  ↑ NO left border    NO vertical lines between columns    NO right border ↑
```

Note: The left/right edges shown above are only for the ASCII diagram — the actual 
table should have NO left or right borders. It's an open, borderless look with only 
horizontal structure.

## Cell Padding
- Top/Bottom padding: 0.06–0.08"
- Left/Right padding: 0.10–0.15"
- This generous padding ensures text doesn't crowd cell edges and provides the 
  column separation that replaces vertical lines

## Column Alignment
- Text columns: Left-aligned
- Numeric columns: Right-aligned (or center-aligned)
- Header alignment: Match the column alignment of body cells below
