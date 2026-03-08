# McKinsey Table Styling — Detailed Border & Format Rules

## ⚠️ WHY THIS MATTERS
Generic "spreadsheet-style" tables with uniform gridlines are the #1 table styling failure. McKinsey tables use a **border hierarchy** that visually separates the header from data and creates a clean, professional look. Getting this right is a Patronus-checked requirement.

## The McKinsey Table Border Hierarchy

### Rule: Borders have 3 distinct levels of visual weight

| Border Location | Weight | Color | Purpose |
|----------------|--------|-------|---------|
| Header row bottom | **2pt** | Navy `#003A70` | **Signature element** — separates header from data |
| Table bottom (last row) | **1pt** | Navy `#003A70` | Provides clean visual closure |
| Header row top | **1pt** | Navy `#003A70` | Optional — defines table top edge |
| Internal row separators | **0.5pt** | Light grey `#D9D9D9` | Subtle — guides the eye without dominating |
| Vertical gridlines | **0.5pt or NONE** | Light grey `#D9D9D9` | Minimal — omit for cleaner look |
| Left/right outer edges | **NONE** | — | Table floats on white background |

### Visual Reference:
```
                                                          ← NO left/right outer borders
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 1pt navy top edge (optional)
    Metric          Current    Target     Gap             ← Header: #F2F2F2 fill, navy bold 11pt
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 2pt NAVY — THE KEY ELEMENT
    Capacity (GW)   0.5        10.0       9.5             ← White fill, #333333 text, 10-11pt
  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← 0.5pt grey (barely visible)
    Investment (€B) 1.2        15.0       13.8
  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← 0.5pt grey (barely visible)
    Jobs (000s)     2.1        15.0       12.9
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 1pt navy bottom closure
                                                          ← NO left/right outer borders
```

## Header Row Formatting
- **Fill**: Light grey `#F2F2F2`
- **Text**: Navy `#003A70`, bold, 11pt, Calibri/Arial
- **Bottom border**: **2pt solid navy `#003A70`** — this is non-negotiable
- **Text alignment**: Left-align category/text columns, right-align number columns
- **Row height**: 0.4" minimum

## Data Row Formatting
- **Fill**: White `#FFFFFF` (or optional very subtle alternating `#F9F9F9`)
- **Text**: Dark grey `#333333`, regular weight, 10–11pt
- **Internal borders**: 0.5pt, `#D9D9D9` — horizontal separators only (preferred)
- **Row height**: 0.35" minimum
- **Cell padding**: 0.05" on all sides minimum

## Column Alignment Rules
- **First column** (categories/labels): Left-aligned
- **Number columns**: Right-aligned
- **Text columns**: Left-aligned
- **Header alignment**: Match the alignment of the data below

## What NOT To Do

### ❌ Generic/Spreadsheet Style (WRONG):
- All borders same 0.75pt weight
- All borders same grey color
- Heavy outer box border around entire table
- Looks like it was copied from Excel

### ❌ Over-Styled (WRONG):
- Bright colored cell fills (teal, blue, green)
- Thick dark borders on every cell
- Rounded corners or shadows on table
- Gradient fills

### ❌ Under-Styled (WRONG):
- No borders at all (data runs together)
- No header differentiation
- No fill on header row

## Python-PPTX Implementation Guide

### Setting Up McKinsey-Style Table Borders
```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from lxml import etree

def set_cell_border(cell, side, width_pt, color_hex):
    """Set a specific border on a table cell.
    side: 'top', 'bottom', 'left', 'right'
    width_pt: border width in points (e.g., 2.0 for thick, 0.5 for thin)
    color_hex: color as hex string without # (e.g., '003A70')
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    side_map = {'top': 'a:lnT', 'bottom': 'a:lnB', 'left': 'a:lnL', 'right': 'a:lnR'}
    nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    
    # Remove existing border of this type
    for existing in tcPr.findall(side_map[side], nsmap):
        tcPr.remove(existing)
    
    ln = etree.SubElement(tcPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}' + side_map[side].split(':')[1])
    ln.set('w', str(int(width_pt * 12700)))  # Convert pt to EMU
    ln.set('cmpd', 'sng')
    
    solidFill = etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    srgbClr = etree.SubElement(solidFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    srgbClr.set('val', color_hex)

def set_no_border(cell, side):
    """Remove a border from a cell."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    side_map = {'top': 'lnT', 'bottom': 'lnB', 'left': 'lnL', 'right': 'lnR'}
    
    ln = etree.SubElement(tcPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}' + side_map[side])
    noFill = etree.SubElement(ln, '{http://schemas.openxmlformats.org/drawingml/2006/main}noFill')

# Apply McKinsey style to a table:
def apply_mckinsey_table_style(table, num_header_rows=1):
    rows = table.rows
    cols = table.columns
    
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row.cells):
            if row_idx < num_header_rows:
                # HEADER ROW: thick navy bottom border
                set_cell_border(cell, 'bottom', 2.0, '003A70')
                set_cell_border(cell, 'top', 1.0, '003A70')
                set_no_border(cell, 'left')
                set_no_border(cell, 'right')
                # Set header fill
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2)
            elif row_idx == len(rows) - 1:
                # LAST ROW: navy bottom border for closure
                set_cell_border(cell, 'bottom', 1.0, '003A70')
                set_cell_border(cell, 'top', 0.5, 'D9D9D9')
                set_no_border(cell, 'left')
                set_no_border(cell, 'right')
            else:
                # DATA ROWS: subtle grey separators
                set_cell_border(cell, 'bottom', 0.5, 'D9D9D9')
                set_cell_border(cell, 'top', 0.5, 'D9D9D9')
                set_no_border(cell, 'left')
                set_no_border(cell, 'right')
```

## Quick Reference Card
When creating any data table, remember:
1. ✅ **2pt navy line under header** — the signature McKinsey element
2. ✅ **0.5pt grey internal lines** — subtle, minimal
3. ✅ **1pt navy line at table bottom** — clean closure
4. ✅ **No outer left/right borders** — table floats cleanly
5. ✅ **#F2F2F2 header fill** — subtle differentiation
6. ✅ **No vertical gridlines** (preferred) — cleaner horizontal-only look
7. ❌ **Never use uniform-weight borders** — that's Excel, not McKinsey
