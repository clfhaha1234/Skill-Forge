# Footer & Structural Elements — Mandatory on Every Slide

## ⚠️ CRITICAL: These Elements are REQUIRED — Patronus-Checked
The footer is checked by automated validation. Missing or malformed footers cause automatic FAIL.

## Slide Structure (Top to Bottom) — With Exact Coordinates

### 1. Title Area (Top)
- Position: x=0.5", y=0.4", width=8.5", height=0.7"
- Insight-driven title in Georgia, 18–22pt, bold, navy (#003A70)
- Left-aligned
- Must NOT extend below y=1.1"

### 2. Thin Divider Line
- **MANDATORY** — never omit this
- Position: y=1.2", from x=0.5" to x=9.5"
- Style: solid line, 0.75–1pt weight
- Color: light grey `#CCCCCC` or `#999999`
- Must have visible gap (0.1") below title text

### 3. Body Content Area
- Position: y=1.4" to y=6.5" (5.1" of vertical space)
- The main content: tables, charts, text, diagrams
- Clean, minimal styling (see DESIGN_RULES.md)
- Use thin borders, no heavy fills, white background
- **MUST include a structured data table when presenting data** (see LAYOUT_PATTERNS.md)
- **Content MUST NOT extend below y=6.5"** — this prevents overlap with source/footer

### 4. Source Attribution
- Position: x=0.5", y=6.6", width=8.5"
- Format: `Source: [description]; McKinsey analysis`
- Font: Calibri/Arial, 8–9pt, regular
- Color: medium grey `#666666`
- Alignment: LEFT-aligned (never centered)
- **Must be at least 0.1" below the lowest body content element**
- **Must be at least 0.1" above the footer divider line**

### 5. Footer Divider Line
- **MANDATORY** — never omit this
- Position: y=6.9", from x=0.5" to x=9.5"
- Style: solid line, 0.5–0.75pt weight
- Color: light grey `#CCCCCC`

### 6. Footer Area (Bottom)
- **MANDATORY** — never omit this
- Position: y=7.0"–7.2"
- Left side (x=0.5"): `CONFIDENTIAL` in 8pt grey
- Right side (x=9.0", right-aligned): Page number (e.g., `1`) in 8pt grey
- Font: Calibri/Arial, 8pt
- Color: `#666666`

## Exact Spacing Summary (Memorize This)

```
y = 0.4"   ┌─ Title starts here
y = 1.1"   └─ Title must end by here (max)
y = 1.2"   ── Divider line
y = 1.4"   ┌─ Body content starts
y = 6.5"   └─ Body content STOPS here (hard limit)
y = 6.6"   ── Source text ("Source: ...")
y = 6.9"   ── Footer divider line
y = 7.0"   ── Footer text (CONFIDENTIAL ... page #)
y = 7.5"   ── Slide bottom edge
```

## Footer Content Format
The footer MUST contain exactly these elements:
- **Left**: "CONFIDENTIAL" (or "STRICTLY CONFIDENTIAL") — 8pt, `#666666`, left-aligned at x=0.5"
- **Right**: Page number as a plain number (e.g., "1") — 8pt, `#666666`, right-aligned at x=9.5"
- **Between divider lines**: The footer text sits between the footer divider line (above) and the slide bottom

## Checklist Before Finalizing Any Slide
- [ ] Background is pure white (#FFFFFF)
- [ ] Title is an insight-driven statement (not a topic label)
- [ ] Title is 18–22pt and does NOT overflow past y=1.1"
- [ ] Thin divider line present at y=1.2"
- [ ] Body content uses only navy/grey/white palette
- [ ] Body content includes a structured data table (when data is present)
- [ ] No thick borders or solid colored fills
- [ ] Body content stops by y=6.5" (does not bleed into footer zone)
- [ ] Source text is present, left-aligned, at y=6.6" in grey
- [ ] Footer divider line present at y=6.9"
- [ ] Footer has "CONFIDENTIAL" (left) and page number (right) at y=7.0"
- [ ] **NO overlapping elements anywhere on the slide**
- [ ] **NO truncated text anywhere on the slide**
- [ ] Overall impression is clean, minimal, and professional
