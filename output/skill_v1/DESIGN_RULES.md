# Design Rules v1 — Fix Critical Issues from v0 Evaluation

## v0 Weaknesses to Fix (from LLM evaluator, scored 25/100)
- Dark navy background used for content slide → must be WHITE
- Teal/cyan accent color is wrong → use navy (#0C2340), white, grey only
- Title is a topic label → must state a conclusion/insight ("so-what" style)
- No structured data table → add a data table with metrics
- Missing McKinsey footer → add thin rule + source (left) + "McKinsey & Company" bold (right) + page number
- Missing crimson divider line below title → add thin red line (#C00000)
- Teal footer bar is wrong → remove, use simple thin rule + text
- Large empty space → fill with structured content

## Layout
- WHITE background (#FFFFFF) — mandatory for data/content slides
- 0.5" margins all sides
- Title area: y=0.4, left-aligned
- Thin crimson divider (#C00000, 1pt) at y=1.15, separated from title by whitespace
- Subtitle in grey below title, above divider

## Color Palette (RESTRAINED — max 3 colors)
- Primary: Dark navy (#0C2340) for timeline, nodes, text
- Background: White (#FFFFFF)
- Accent: Thin crimson line (#C00000) — ONLY for divider, not large elements
- Body text: Dark grey (#404040)
- Light grey (#E8E8E8) for table row dividers

## Typography
- Title: Georgia Bold 22pt, black (#000000), left-aligned — must be an INSIGHT not a topic
- Subtitle: Calibri 11pt, grey (#666666)
- Body/labels: Calibri 9pt, dark grey (#404040)
- Footnote: Calibri 7pt italic, grey (#999999)

## Title Rule
- Title MUST state a conclusion: "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"
- NOT a topic label like "Dutch Hydrogen Strategy (2020-2035)"

## Timeline
- Horizontal line in dark navy (#0C2340), 1.5pt
- 6 circular nodes, 0.3" diameter, dark navy fill, white text for year labels
- Milestone descriptions: Calibri 8.5pt, dark grey, alternating above/below
- Timeline at y=3.0 (vertically centered in slide)

## Data Table (below timeline)
- 3 rows: Electrolyzer Capacity, Green H2 Cost, H2 Production
- 5 columns: 2020, 2025, 2028, 2030, 2035
- Navy border top+bottom of header row (1.5pt, #0C2340)
- Light grey row dividers (0.5pt, #E8E8E8)
- Bold left column labels, center-aligned values
- Font: Calibri 8pt

## Footer (McKinsey format)
- Thin dark rule line at y=6.85 across full width
- Left: "Source: Dutch National Hydrogen Strategy; REPowerEU; McKinsey Energy Insights" (Calibri 7pt, grey)
- Right: "McKinsey & Company" bold (Calibri 8pt, black) + page number "1"
- NO colored footer bars

## Footnote
- Below table: "1. Capacity and cost projections based on Dutch Government targets and IEA estimates; actual figures may vary depending on policy and market conditions."
- Calibri 7pt italic, grey (#999999)
