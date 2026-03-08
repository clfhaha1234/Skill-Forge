# Design Rules v2 — Refine from v1 Evaluation (89/100)

## v1 Weaknesses to Fix (from LLM evaluator)
- Red divider line too thick → reduce to 0.75pt
- Timeline middle area slightly busy → add more whitespace, simplify node style
- Table header: should use navy border lines (top+bottom) NOT filled navy background
- Subtitle font needs more differentiation → smaller size, lighter color
- Timeline nodes could be more refined

## Changes from v1
- Crimson divider: 0.75pt (was 1pt) — thinner, more subtle
- Table header: NO filled background, use navy border lines top+bottom of header row only (1.5pt #0C2340)
- Table header text: Bold, dark navy, NOT white (since no fill)
- Subtitle: Calibri 10pt (was 11pt), lighter grey (#888888)
- Timeline nodes: slightly smaller (0.28" from 0.3"), cleaner look
- More whitespace between timeline and table sections

## Layout
- WHITE background (#FFFFFF)
- 0.5" margins all sides
- Title: y=0.35, Georgia Bold 22pt, black, left-aligned — MUST be insight/conclusion
- Subtitle: y=1.2, Calibri 10pt, #888888
- Crimson divider: y=1.5, 0.75pt, #C00000
- Timeline area: y=1.8 to y=3.6 (generous whitespace)
- Timeline line: y=2.9
- Data table: y=3.9
- Footnote: y=5.3
- Footer rule: y=6.85

## Color Palette (RESTRAINED — max 3 colors)
- Primary: Dark navy (#0C2340)
- Background: White (#FFFFFF)
- Accent: Crimson (#C00000) — ONLY thin divider line
- Body text: Dark grey (#404040)
- Subtle grey: #E8E8E8 for table row dividers
- NO teal, NO bright colors, NO colored backgrounds

## Typography
- Title: Georgia Bold 22pt, #000000, left-aligned
- Subtitle: Calibri 10pt, #888888
- Timeline labels: Calibri 8.5pt, #404040
- Year labels inside nodes: Calibri Bold 8pt, white (#FFFFFF)
- Table header: Calibri Bold 8.5pt, #0C2340 (no white — no fill)
- Table body: Calibri 8pt, #404040, center-aligned
- Table left column: Calibri Bold 8.5pt, #333333
- Footnote: Calibri 7pt italic, #999999
- Footer source: Calibri 7pt, #999999
- Footer branding: Calibri 8pt bold, #000000

## Title Rule
- "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"

## Timeline
- Horizontal line: dark navy (#0C2340), 1.5pt, y=2.9
- 6 circular nodes: 0.28" diameter, navy fill, white year text (Calibri Bold 8pt)
- Milestone descriptions: alternating above/below, Calibri 8.5pt, #404040
- Clean spacing — no clutter around nodes

## Data Table
- 3 rows: Electrolyzer Capacity (GW), Green H2 Cost (€/kg), H2 Production (kt/yr)
- 5 columns: 2020, 2025, 2028, 2030, 2035
- Header: NO background fill. Navy border lines top (1.5pt) and bottom (1.5pt) of header row
- Header text: Bold, dark navy (#0C2340)
- Body: light grey bottom borders (0.5pt, #E8E8E8)
- Left column labels: bold
- Values: center-aligned
- Navy bottom border on last row (1pt, #0C2340) to close the table

## Footer
- Thin dark rule (0.5pt, #333333) at y=6.85
- Left: source text, Calibri 7pt, #999999
- Right: "McKinsey & Company" Calibri 8pt bold #000000, then "  1"
- NO colored bars
