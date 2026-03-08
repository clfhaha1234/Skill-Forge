# McKinsey Slide Examples

## Example 1: Complete Slide Layout
```
y=0.4"  ┌──────────────────────────────────────────────────────────┐
        │  Three H₂ corridors could position NL as Europe's hub   │  20pt Georgia bold #003A70
y=1.1"  └──────────────────────────────────────────────────────────┘
y=1.2"  ───────────────────────────────────────────────────────────  1pt #CCCCCC

y=1.4"    Category          2025       2030       2035               #F2F2F2 fill, navy bold 11pt
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  2pt #003A70
          Capacity          1 GW       5 GW       10 GW             white fill, #333333, 10pt
        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  0.5pt #D9D9D9
          Investment        €2B        €8B        €15B
        ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  0.5pt #D9D9D9
          Jobs created      3,000      8,000      15,000
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  1pt #003A70
y=6.4"  (content stops)

y=6.75" Source: Government reports; McKinsey analysis               8pt #666666
y=6.9"  ───────────────────────────────────────────────────────────  0.75pt #CCCCCC
y=7.0"  CONFIDENTIAL                        McKinsey & Company   1  8pt #666666
```

## Example 2: Table Border Comparison

### ❌ WRONG — Uniform borders (Excel-style):
```
┌─────────────┬────────┬────────┬────────┐  All borders same weight/color
│ Category    │ 2025   │ 2030   │ 2035   │
├─────────────┼────────┼────────┼────────┤
│ Capacity    │ 1 GW   │ 5 GW   │ 10 GW  │
└─────────────┴────────┴────────┴────────┘
```

### ✅ CORRECT — McKinsey hierarchical borders:
```
  Category        2025       2030       2035       ← #F2F2F2 fill, navy bold
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ← 2pt navy (THICK — signature)
  Capacity        1 GW       5 GW       10 GW     ← white fill, #333333
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← 0.5pt #D9D9D9 (subtle)
  Investment      €2B        €8B        €15B
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ← 1pt navy (closure)
No left/right outer borders — table floats on white
```

## Example 3: Title Quality

| ❌ Wrong (Topic label) | ✅ Correct (Insight statement) |
|----------------------|-------------------------------|
| "Dutch Hydrogen Strategy" | "Three H₂ corridors could position NL as Europe's hub by 2030" |
| "Market Overview" | "Market share erosion accelerated to 3.2pp in Q3" |
| "Cost Analysis" | "Consolidating 4 procurement categories yields €45M savings" |

## Example 4: Timeline Boxes

### ❌ WRONG — Text truncated:
```
┌──────────┐  ┌──────────┐
│National   │  │10 GW tar │  ← CUT OFF!
│Hydrog...  │  │get reac..│
└──────────┘  └──────────┘
```

### ✅ CORRECT — Short labels, details outside:
```
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Phase 1         │  │ Phase 2         │  │ Phase 3         │
│ Foundation      │  │ Scale-up        │  │ Full deploy     │
│ (2024–2026)     │  │ (2027–2030)     │  │ (2031–2035)     │
└────────────────┘  └────────────────┘  └────────────────┘
  1 GW / €2B         5 GW / €8B          10 GW / €15B       ← Details OUTSIDE
```

## Example 5: Footer Format

### ❌ WRONG — No McKinsey branding:
```
CONFIDENTIAL                                              1
```

### ✅ CORRECT — Complete footer:
```
Source: Industry reports; McKinsey analysis          ← y=6.75"
────────────────────────────────────────────────     ← y=6.9"
CONFIDENTIAL                 McKinsey & Company  1  ← y=7.0"
```

## Python-PPTX Table Border Implementation
```python
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from lxml import etree

NSMAP = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def set_cell_border(cell, side, width_pt, color_hex):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tag = {'top': 'lnT', 'bottom': 'lnB', 'left': 'lnL', 'right': 'lnR'}[side]
    # Remove existing
    for existing in tcPr.findall(f'{{{NSMAP}}}{tag}'):
        tcPr.remove(existing)
    ln = etree.SubElement(tcPr, f'{{{NSMAP}}}{tag}')
    ln.set('w', str(int(width_pt * 12700)))
    ln.set('cmpd', 'sng')
    sf = etree.SubElement(ln, f'{{{NSMAP}}}solidFill')
    clr = etree.SubElement(sf, f'{{{NSMAP}}}srgbClr')
    clr.set('val', color_hex)

def set_no_border(cell, side):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tag = {'top': 'lnT', 'bottom': 'lnB', 'left': 'lnL', 'right': 'lnR'}[side]
    ln = etree.SubElement(tcPr, f'{{{NSMAP}}}{tag}')
    etree.SubElement(ln, f'{{{NSMAP}}}noFill')

def apply_mckinsey_table_style(table):
    for row_idx, row in enumerate(table.rows):
        for cell in row.cells:
            set_no_border(cell, 'left')
            set_no_border(cell, 'right')
            if row_idx == 0:  # Header
                set_cell_border(cell, 'top', 1.0, '003A70')
                set_cell_border(cell, 'bottom', 2.0, '003A70')
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xF2, 0xF2, 0xF2)
            elif row_idx == len(table.rows) - 1:  # Last row
                set_cell_border(cell, 'top', 0.5, 'D9D9D9')
                set_cell_border(cell, 'bottom', 1.0, '003A70')
            else:  # Data rows
                set_cell_border(cell, 'top', 0.5, 'D9D9D9')
                set_cell_border(cell, 'bottom', 0.5, 'D9D9D9')
```
