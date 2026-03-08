# Design Rules — McKinsey Consulting Style (v3)

## Changes from v2
- Fix overlapping: table was too tall, footnotes collided with last row
- Reduce title font to 20pt (was rendering at ~36pt due to Georgia Bold sizing)
- Compact table row heights to leave room for footnotes below
- Move footnotes to y=4.7, footer line to y=5.15, footer text to y=5.2
- Ensure total content height: title(0.7) + table(2.8) + gap(0.1) + footnotes(0.4) + gap(0.15) + footer = fits in 5.625

## Background & Layout
- White background (FFFFFF)
- 16:9 (10" x 5.625")
- Margins: 0.5" left/right
- Title area: y=0.15 to y=0.85 (max 0.7" height)
- Divider: y=0.95
- Table area: y=1.2 to y=4.5 (max 3.3" height)
- Footnotes: y=4.55 (max 0.4" height)
- Footer line: y=5.15
- Footer text: y=5.2

## Color Palette
- Text: black (000000)
- Navy accent: 1B3A5C (header borders)
- Blue column header: DCE9F5
- Green column header: E8F6EF
- Data cells: white (FFFFFF)
- Footer/footnotes: grey (666666)
- Table borders: C0C0C0 (0.75pt)

## Typography
- Title: Georgia Bold, 20pt, black
- Subtitle: Calibri, 10pt, #666666
- Table header: Calibri Bold, 10pt
- Table body: Calibri, 9pt
- Footnotes: Calibri, 6pt, #666666
- Footer: Calibri, 8pt, #666666

## Title
- Insight "so-what" conclusion
- Section numbering "1.1/" prefix
- Max 2 lines

## Table
- 2pt navy top border on header row
- Header: bold, centered, light color fills for highlighted columns
- Data cells: white, left-aligned
- Row borders: 0.75pt grey
- Row labels: bold, left column
- Compact row heights (0.3-0.55") to prevent overflow

## Structural
- Divider line: 1pt dark grey below title
- "Low-carbon H2" or equivalent label centered above relevant columns
- Footer line: 0.5pt dark grey
- "McKinsey & Company    N" right-aligned
- Footnotes: compact, 6pt, numbered
