# Design Rules — McKinsey Consulting Style (v5)

## Changes from v4
- Table borders: horizontal only, NO vertical borders (McKinsey style)
- Remove filler paragraph text — data should fill the space
- Make table taller to fill content area (avoid dead space)
- Add row category labels with left-aligned column color indicators (like ref-05)
- Use borderH for horizontal borders, set borderV to none

## Background & Layout
- White background (FFFFFF)
- 16:9 (10" x 5.625")
- Margins: 0.5" left/right

## Layout Positions
- Title: x=0.5, y=0.2, h=0.65
- Subtitle: x=0.5, y=0.88, h=0.18
- Divider line: y=1.1
- Table: y=1.3, fills down to y=4.6 (use the space)
- Footnotes: y=4.65, h=0.3
- Footer line: y=5.1
- Footer text: y=5.15

## Color Palette (RESTRAINED)
- Text: black (000000) or dark grey (333333)
- Navy accent: 1B3A5C (2pt header top border)
- ALL cells: white (FFFFFF)
- Horizontal row borders: D0D0D0 (0.5pt)
- NO vertical borders
- Footer/footnotes: 666666

## Typography
- Title: Georgia Bold, 16pt, black
- Subtitle: Calibri, 9pt, #666666
- Table header: Calibri Bold, 9pt, black
- Table body: Calibri, 9pt, #333333
- Row year labels: Calibri Bold, 10pt, black
- Footnotes: Calibri, 6pt, #666666
- Footer: Calibri, 8pt, #666666

## Table Style
- HORIZONTAL borders only — no vertical lines
- Use PptxGenJS border array: [top, right, bottom, left]
  - Header row bottom: { pt: 1, color: "333333" }
  - Data row bottom: { pt: 0.5, color: "D0D0D0" }
  - Left/right borders: { pt: 0, color: "FFFFFF" } (invisible)
- 2pt navy line above header (as separate shape)
- Column headers: bold, centered
- Row labels: bold, left-aligned
- Use color indicator squares (filled/outline) for least-cost marking

## Structural
- Divider: 1pt dark grey below title
- Footer: "McKinsey & Company    N" right-aligned
- Footnotes: compact numbered source citations
