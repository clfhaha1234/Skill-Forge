# Design Rules v5 — Remove Red Line + Space Optimization (v4: 89/100)

## v4 Weaknesses to Fix (from LLM evaluator)
- Font appears sans-serif for title → ensure Georgia (serif) renders
- Too much white space below content → better vertical distribution
- Timeline takes too much space → compact it
- Table metric labels could be bolder
- Connector line slightly thin

## Critical Fix: RED LINE IS WRONG
- Looking at McKinsey reference data slides (ref-04), there is NO crimson/red divider
- The line below the title is a THIN DARK GREY rule (#333333), not crimson
- Remove all crimson/red from the slide entirely

## Changes from v4
- Divider line: dark grey (#333333) 0.75pt instead of crimson (#C00000)
- Title font: explicitly Georgia (serif) — critical for McKinsey look
- Better vertical space distribution: tighter timeline, less dead space at bottom
- Table left column labels: bolder weight
- Timeline connector: 2pt navy (keep from v4)
- Move content up slightly to reduce bottom white space

## Layout (13.33" × 7.5" — LAYOUT_16x9)
- WHITE background (#FFFFFF)
- 0.5" margins all sides
- Title: y=0.3, x=0.5, Georgia Bold 22pt, black
- Subtitle: y=1.2, x=0.5, Calibri 10pt, #888888
- Divider: y=1.45, 0.75pt, DARK GREY (#333333) — NOT red/crimson
- Timeline area: y=1.7 to y=3.3 (more compact)
- Timeline line: y=2.6, 2pt navy
- Data table: y=3.5
- Footnote: y=5.0
- Footer rule: y=6.4 (0.5pt, #333333)
- Footer text: y=6.45

## Color Palette (RESTRAINED — NO RED)
- Dark navy (#0C2340): timeline, nodes, table header borders
- White (#FFFFFF): background
- Dark grey (#333333): divider line, footer rule
- Body text grey (#404040)
- Light grey (#E8E8E8): table row dividers
- Medium grey (#999999): footnote, source
- **NO crimson, NO red, NO teal, NO bright colors**

## Typography
- Title: Georgia Bold 22pt, #000000 — MUST be serif font
- Subtitle: Calibri 10pt, #888888
- Year labels in nodes: Calibri Bold 7.5pt, white
- Milestone labels: Calibri 8.5pt, #404040
- Table header: Calibri Bold 9pt, #0C2340 (NO fill)
- Table body: Calibri 8pt, #404040, center-aligned
- Table left column: Calibri Bold 9pt, #222222 (darker, bolder)
- Footnote: Calibri 6.5pt italic, #999999
- Source: Calibri 7pt, #999999
- Branding: Calibri 8pt bold, #000000

## Title
- "The Netherlands aims to become Europe's green hydrogen hub, scaling from 500 MW to 3-4 GW by 2030"

## Timeline
- Navy line (#0C2340), 2pt, y=2.6
- 6 nodes: 0.26" circles, navy fill, white year text
- Alternating above/below descriptions
- Thin vertical tick marks (1pt, navy)

## Data Table
- Header: NO fill. Navy border top+bottom (1.5pt #0C2340)
- Header text: bold navy 9pt
- Body: light grey bottom borders (0.5pt #E8E8E8)
- Last row: navy bottom border (1pt #0C2340)
- ALL data values center-aligned
- Left column: bold 9pt, dark (#222222)
- 3 metrics × 5 years

## Footer (MUST be visible)
- Rule at y=6.4 (0.5pt, #333333)
- y=6.45: Source left, "McKinsey & Company" bold + "  1" right
