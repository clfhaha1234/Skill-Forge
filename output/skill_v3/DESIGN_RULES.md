# Design Rules v3 — Fix Footer + Polish from v2 Evaluation (86/100)

## v2 Weaknesses to Fix (from LLM evaluator)
- Missing McKinsey footer (rule + branding + page number) — was placed too low, got cut off → move up
- Crimson divider too close to subtitle → add more whitespace
- Timeline circles feel heavy → consider slightly smaller or outline style
- Table values not well center-aligned → ensure proper alignment
- Uses "Note:" instead of numbered footnote → use "1." prefix
- Too much empty space below note → tighten layout, bring footer up

## Changes from v2
- Footer moved UP: rule at y=6.6, source at y=6.65, branding at y=6.65 (was y=6.85-6.9)
- Footnote uses numbered style: "1. Capacity and cost..." not "Note: ..."
- Crimson divider moved down slightly: y=1.55 (more space from subtitle at y=1.2)
- Timeline nodes: 0.26" diameter (slightly smaller, less heavy)
- Table values: explicitly center-aligned
- Less dead space at bottom by tightening gap between footnote and footer

## Layout (slide is 13.33" x 7.5" — LAYOUT_16x9)
- WHITE background (#FFFFFF)
- 0.5" margins all sides
- Title: y=0.35, x=0.5
- Subtitle: y=1.25, x=0.5
- Crimson divider: y=1.55 (thin line, 0.75pt, #C00000)
- Timeline area: y=2.0 to y=3.6
- Timeline line: y=2.9, 1.5pt navy
- Data table: y=3.9
- Footnote: y=5.5, numbered "1. ..."
- Footer rule: y=6.6 (0.5pt, #333333)
- Footer text: y=6.65 — source left, "McKinsey & Company" + "1" right

## Color Palette (RESTRAINED)
- Dark navy (#0C2340): timeline, nodes, table header borders
- White (#FFFFFF): background
- Crimson (#C00000): thin divider line ONLY
- Dark grey (#404040): body text
- Light grey (#E8E8E8): table row dividers
- Medium grey (#999999): footnote, source text

## Typography
- Title: Georgia Bold 22pt, #000000
- Subtitle: Calibri 10pt, #888888
- Year labels in nodes: Calibri Bold 7.5pt, white
- Milestone labels: Calibri 8.5pt, #404040
- Table header: Calibri Bold 8.5pt, #0C2340 (no background fill)
- Table body: Calibri 8pt, #404040, center-aligned
- Table left column: Calibri Bold 8.5pt, #333333
- Footnote: Calibri 7pt italic, #999999, starts with "1."
- Source: Calibri 7pt, #999999
- Branding: Calibri 8pt bold, #000000

## Title
- "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"

## Timeline
- Navy line (#0C2340), 1.5pt
- 6 nodes: 0.26" circles, navy fill, white year text
- Alternating above/below milestone descriptions

## Data Table
- Header: NO fill. Navy border top (1.5pt) + bottom (1.5pt) on header row
- Header text: bold navy
- Body rows: light grey bottom borders (0.5pt #E8E8E8)
- Last row: navy bottom border (1pt #0C2340)
- Values center-aligned
- 3 metrics × 5 years

## Footer (MUST be visible — critical fix)
- Thin dark rule at y=6.6 (0.5pt, #333333), x=0.5 to x=12.83
- Source text at y=6.65, x=0.5: "Source: Dutch National Hydrogen Strategy; REPowerEU; McKinsey Energy Insights"
- Branding at y=6.65, right-aligned near x=12.5: "McKinsey & Company" bold + "  1"
