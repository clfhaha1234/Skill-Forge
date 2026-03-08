# Design Rules v4 — Final Polish from v3 Evaluation (91/100)

## v3 Weaknesses to Fix (from LLM evaluator)
- Timeline connector line could be thicker/more refined → increase to 2pt
- Table data values need better center-alignment
- Footnote text could be smaller and more precisely positioned
- Vertical spacing between timeline and table too generous → tighten

## Changes from v3
- Timeline connector: 2pt (was 1.5pt) for more polished look
- Table values: explicitly set align:"center" on every data cell
- Footnote: Calibri 6.5pt (was 7pt), positioned closer to table at y=5.2 (was y=5.5)
- Timeline-to-table gap: table moved up to y=3.7 (was y=3.9)
- Footer moved up slightly: rule at y=6.45, text at y=6.5

## Layout (13.33" × 7.5" — LAYOUT_16x9)
- WHITE background (#FFFFFF)
- 0.5" margins all sides
- Title: y=0.35, x=0.5
- Subtitle: y=1.25, x=0.5
- Crimson divider: y=1.55, 0.75pt, #C00000
- Timeline area: y=2.0 to y=3.5
- Timeline line: y=2.8, 2pt navy
- Data table: y=3.7
- Footnote: y=5.2
- Footer rule: y=6.45 (0.5pt, #333333)
- Footer text: y=6.5

## Color Palette (RESTRAINED)
- Dark navy (#0C2340): timeline, nodes, table header borders
- White (#FFFFFF): background
- Crimson (#C00000): thin divider line ONLY
- Dark grey (#404040): body text
- Light grey (#E8E8E8): table row dividers
- Medium grey (#999999): footnote, source

## Typography
- Title: Georgia Bold 22pt, #000000
- Subtitle: Calibri 10pt, #888888
- Year labels in nodes: Calibri Bold 7.5pt, white
- Milestone labels: Calibri 8.5pt, #404040
- Table header: Calibri Bold 8.5pt, #0C2340 (NO fill)
- Table body: Calibri 8pt, #404040, center-aligned
- Table left column: Calibri Bold 8.5pt, #333333, left-aligned
- Footnote: Calibri 6.5pt italic, #999999
- Source: Calibri 7pt, #999999
- Branding: Calibri 8pt bold, #000000

## Title
- "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"

## Timeline
- Navy line (#0C2340), 2pt, y=2.8
- 6 nodes: 0.26" circles, navy fill, white year text
- Alternating above/below descriptions
- Thin vertical tick marks (1pt, navy, 0.15" tall) connecting to labels

## Data Table
- Header: NO fill. Navy border top+bottom (1.5pt #0C2340)
- Header text: bold navy, center-aligned (except "Metric" label left-aligned)
- Body: light grey bottom borders (0.5pt #E8E8E8)
- Last row: navy bottom border (1pt #0C2340)
- ALL data values: align:"center"
- Left column labels: bold, left-aligned
- 3 metrics: Electrolyzer capacity (GW), Green H2 cost (EUR/kg), H2 production (kt/yr)
- 5 year columns: 2020, 2025, 2028, 2030, 2035

## Footer (MUST be visible)
- Rule line at y=6.45 (0.5pt, #333333), x=0.5 to x=12.83
- y=6.5: Source left, "McKinsey & Company" bold + "  1" right
