# Layout Patterns — Precise Element Positioning

## Standard Slide Dimensions
- Width: 13.333" (widescreen 16:9)
- Height: 7.5"

## Zone Map (Vertical)
All Y-coordinates are from the top of the slide:

| Zone | Y Start | Y End | Contents |
|------|---------|-------|----------|
| Top margin | 0" | 0.55" | Empty |
| Title | 0.55" | 1.05" | Title text (22–26pt, bold) |
| Divider line | 1.10" | 1.12" | Horizontal rule, navy or gray |
| Content | 1.25" | 6.50" | Tables, charts, text blocks |
| Footer line | 6.55" | 6.57" | Thin gray separator |
| Footer text | 6.60" | 7.10" | Source (left), page number (right) |
| Bottom margin | 7.10" | 7.50" | Empty |

## Zone Map (Horizontal)
| Zone | X Start | X End | Contents |
|------|---------|-------|----------|
| Left margin | 0" | 0.75" | Empty |
| Content area | 0.75" | 12.58" | All content lives here |
| Right margin | 12.58" | 13.33" | Empty |

**Content width**: 11.83" (= 12.58 - 0.75)

## Title Block Pattern
```
Position: X=0.75", Y=0.55", W=11.83", H=0.50"
Text: Insight-driven "so-what" statement
Font: Arial/Calibri, 22–26pt, Bold, color #333333
Alignment: Left
```

## Divider Line Pattern
```
Start: X=0.75", Y=1.12"
End:   X=12.58", Y=1.12"
Color: #003A70 (navy) — weight 1.5pt
```

## Data Table Pattern (Full-Width)
```
Position: X=0.75", Y=1.35", W=11.83"
Height: varies by row count — typically 0.35–0.45" per row
Header row: Fill #003A70, text white #FFFFFF, 11pt bold
Body rows: Alternating #FFFFFF and #F2F2F2, text #333333, 10–12pt
Borders: 0.75pt, color #D6DCE4
```

### Row height calculation:
- Header: 0.40"
- Body rows: 0.35–0.40" each
- Max rows before overflow: ~13 rows (to stay above footer at Y=6.50")
- If more rows needed, reduce row height to 0.30" minimum or split across slides

## Data Table Pattern (Two-Column)
For comparison layouts, place two tables side by side:
```
Left table:  X=0.75", Y=1.35", W=5.67"
Right table: X=6.58", Y=1.35", W=5.67"
Gap between: 0.25"
```

## Text Block Pattern
```
Position: X=0.75", Y=1.35", W=11.83"
Font: Arial/Calibri, 12–14pt, color #333333
Line spacing: 1.15–1.3
```

## Callout Box Pattern (Key Insight)
```
Position: X=0.75", Y=varies, W=11.83", H=0.6"
Fill: #F2F6FA (very light blue) or #F5F5F5 (light gray)
Border: 1pt #4472C4 (left border only, for accent)
Text: 12–14pt, color #333333
```

## Footer Pattern
```
Source text:
  Position: X=0.75", Y=6.65", W=10.0", H=0.35"
  Text: "Source: [attribution]"
  Font: Arial 8pt, italic, color #999999, left-aligned

Page number:
  Position: X=11.83", Y=6.65", W=1.5", H=0.35"
  Text: "1" (or appropriate number)
  Font: Arial 8pt, color #999999, right-aligned

Footer separator line:
  Start: X=0.75", Y=6.55"
  End:   X=12.58", Y=6.55"
  Color: #D6DCE4, weight 0.5pt
```

## Anti-Overlap Rules
1. Never place two text boxes that share any overlapping rectangular area
2. When calculating positions, account for text wrap — a long title at 24pt in a box W=11.83" may need H=0.60" if it wraps to 2 lines
3. Leave at least 0.10" vertical gap between any two adjacent elements
4. If content exceeds the content zone (below Y=6.50"), either:
   - Reduce font sizes (but never below minimums)
   - Split content across multiple slides
   - Summarize/condense the information
