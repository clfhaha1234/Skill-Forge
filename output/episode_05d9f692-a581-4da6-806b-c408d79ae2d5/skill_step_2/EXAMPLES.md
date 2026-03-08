# Examples of Correct McKinsey-Style Slides

## Example 1: Title Construction (Keep Titles Concise)

### ❌ WRONG (Generic topic label):
```
Dutch Hydrogen Strategy
```

### ❌ WRONG (Too long — will wrap/overflow at 20pt):
```
The Netherlands can unlock €15B in economic value by 2035 through prioritized 
investment in three green hydrogen corridors across the northern provinces
```

### ✅ CORRECT (Insight-driven AND concise — fits in 1–2 lines at 20pt):
```
NL can unlock €15B by 2035 through three green hydrogen corridor investments
```
(~75 characters — fits perfectly on one line at 20pt in an 8.5" text box)

### ✅ CORRECT (Another concise example):
```
Accelerating electrolyzer deployment by 2 years cuts import dependency 40%
```

**Rules**: 
- Title must tell the reader the key takeaway
- Keep under 120 characters to prevent wrapping overflow
- Use 18–22pt font (NOT 24–28pt)

---

## Example 2: Full Slide Layout (ASCII with Y-coordinates)

```
y=0.4"  ┌──────────────────────────────────────────────────────────┐
        │  NL can unlock €15B by 2035 through three H₂ corridors  │  ← 20pt Georgia bold navy
y=1.1"  └──────────────────────────────────────────────────────────┘
y=1.2"  ───────────────────────────────────────────────────────────   ← thin grey divider (1pt)

y=1.4"  ┌──────────────────────────────────────────────────────────┐
        │                                                          │
        │  [BODY CONTENT: structured data table, timeline, etc.]   │
        │                                                          │
        │  ┌────────────┬────────────┬────────────┬────────────┐   │
        │  │ Category   │ 2025       │ 2030       │ 2035       │   │  ← Table with gridlines
        │  ├────────────┼────────────┼────────────┼────────────┤   │
        │  │ Capacity   │ 1 GW       │ 5 GW       │ 10 GW      │   │
        │  ├────────────┼────────────┼────────────┼────────────┤   │
        │  │ Investment │ €2B        │ €8B        │ €15B       │   │
        │  └────────────┴────────────┴────────────┴────────────┘   │
        │                                                          │
y=6.5"  └──────────────────────────────────────────────────────────┘  ← CONTENT STOPS HERE

y=6.6"  Source: Government reports; McKinsey analysis                 ← 8pt grey, left-aligned

y=6.9"  ───────────────────────────────────────────────────────────   ← thin grey footer line

y=7.0"  CONFIDENTIAL                                           1     ← 8pt grey, left + right
y=7.5"  ─── slide bottom edge ───
```

**Key points**: 
- Title stays above y=1.1"
- Body content stays between y=1.4" and y=6.5"
- Source, footer line, and footer text are in FIXED positions below content
- Nothing overlaps anything else

---

## Example 3: Color Usage

### Correct palette application:
- Title text: `#003A70` (navy), 18–22pt
- Body text: `#333333` (dark grey), 10–12pt
- Table headers: `#003A70` navy text on `#F2F2F2` very light grey background
- Table gridlines: `#D9D9D9` (light grey), 0.75pt
- Highlighted data: `#0072CE` (McKinsey blue) — used sparingly
- Footer/source text: `#666666` (medium grey), 8pt
- All backgrounds: `#FFFFFF` (white)

### NEVER use:
- `#028090` (teal), `#00A896` (seafoam), `#02C39A` (mint)
- Any saturated or vibrant fill colors

---

## Example 4: Structured Data Table (REQUIRED for data slides)

### ❌ WRONG:
- Free-floating text boxes with numbers scattered around
- Thick dark borders around cells
- Solid teal/blue cell fills

### ✅ CORRECT:
```
┌─────────────────┬──────────┬──────────┬──────────┐
│ Metric          │ Current  │ Target   │ Gap      │  ← Header: #F2F2F2 fill, navy bold
├─────────────────┼──────────┼──────────┼──────────┤     Gridlines: #D9D9D9, 0.75pt
│ Capacity (GW)   │ 0.5      │ 10.0     │ 9.5      │  ← White fill, grey text, 10pt
├─────────────────┼──────────┼──────────┼──────────┤
│ Investment (€B)  │ 1.2      │ 15.0     │ 13.8     │
├─────────────────┼──────────┼──────────┼──────────┤
│ Jobs (000s)      │ 2.1      │ 15.0     │ 12.9     │
└─────────────────┴──────────┴──────────┴──────────┘
```
- Cell padding: 0.05" minimum (text must never touch cell edges)
- Row height: 0.35" minimum
- Numbers right-aligned, text left-aligned

---

## Example 5: Timeline/Process Flow — Text Fitting

### ❌ WRONG (Text truncation — THE MOST COMMON ERROR):
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│National   │  │10 GW tar │  │Green hyd │   ← TEXT IS CUT OFF!
│Hydrog...  │  │get reac..│  │rogen exp.│   ← UNACCEPTABLE
└──────────┘  └──────────┘  └──────────┘
```

### ❌ WRONG (Icons overlap text):
```
┌──────────┐
│🏭Nat'l H₂│   ← Icon and text collide
└──────────┘
```

### ✅ CORRECT (Short labels, properly sized boxes):
```
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Phase 1         │  │ Phase 2         │  │ Phase 3         │
│ Foundation      │  │ Scale-up        │  │ Full deploy     │
│ (2024–2026)     │  │ (2027–2030)     │  │ (2031–2035)     │
└────────────────┘  └────────────────┘  └────────────────┘
  1 GW target        5 GW target         10 GW target        ← Details OUTSIDE boxes
  €2B investment     €8B investment      €15B investment
```

**Rules for timeline boxes**:
- Use SHORT labels inside (2–4 words per line)
- Put detailed text BELOW or BESIDE boxes, not crammed inside
- Font inside boxes: 9–10pt (NOT 12–14pt)
- NO icons inside boxes — use text only
- Box minimum size: 1.5" wide × 0.7" tall
- If > 5 phases, switch to vertical list layout

---

## Example 6: Bottom Summary Metrics (Non-Overlapping)

### ❌ WRONG (Metrics overlap with source text):
```
│ €15B value  │ │ 10 GW      │ │ 15,000 jobs │
Source: Government reports                          ← OVERLAPPING!
```

### ✅ CORRECT (Clear separation):
```
y=5.0"  ┌────────────┐  ┌────────────┐  ┌────────────┐
        │   €15B      │  │   10 GW     │  │  15,000     │
        │ total value │  │ capacity    │  │  new jobs   │
y=6.3"  └────────────┘  └────────────┘  └────────────┘
                                                           ← 0.3" gap
y=6.6"  Source: Government reports; McKinsey analysis      ← clearly separated
y=6.9"  ────────────────────────────────────────────────
y=7.0"  CONFIDENTIAL                                  1
```

**Rule**: Body content (including bottom metrics) must STOP by y=6.5". Source starts at y=6.6".
