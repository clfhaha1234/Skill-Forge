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
        │    Category          2025       2030       2035          │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  ← 2pt navy header border
        │    Capacity          1 GW       5 GW       10 GW        │
        │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  ← 0.5pt grey (subtle)
        │    Investment        €2B        €8B        €15B         │
        │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │  ← 0.5pt grey (subtle)
        │    Jobs created      3,000      8,000      15,000       │
        │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  ← 1pt navy bottom border
        │                                                          │
y=6.4"  └──────────────────────────────────────────────────────────┘  ← CONTENT STOPS HERE

y=6.75" Source: Government reports; McKinsey analysis                 ← 8pt grey, anchored near bottom

y=6.9"  ───────────────────────────────────────────────────────────   ← thin grey footer line

y=7.0"  CONFIDENTIAL                        McKinsey & Company   1   ← 8pt grey
y=7.5"  ─── slide bottom edge ───
```

**Key points**: 
- Title stays above y=1.1"
- Body content stays between y=1.4" and y=6.4"
- Source anchors near the bottom at y=6.75" (close to footer line)
- Footer includes "McKinsey & Company" branding in bottom-right
- Nothing overlaps anything else

---

## Example 3: Color Usage

### Correct palette application:
- Title text: `#003A70` (navy), 18–22pt
- Body text: `#333333` (dark grey), 10–12pt
- Table headers: `#003A70` navy text on `#F2F2F2` very light grey background
- **Table header bottom border: `#003A70` navy, 2pt** — signature McKinsey style
- Table internal gridlines: `#D9D9D9` (light grey), **0.5pt** — minimal and subtle
- Table bottom border: `#003A70` navy, 1pt
- Highlighted data: `#0072CE` (McKinsey blue) — used sparingly
- Footer/source text: `#666666` (medium grey), 8pt
- All backgrounds: `#FFFFFF` (white)

### NEVER use:
- `#028090` (teal), `#00A896` (seafoam), `#02C39A` (mint)
- Any saturated or vibrant fill colors
- Uniform-weight gridlines that make tables look like Excel spreadsheets

---

## Example 4: Structured Data Table — McKinsey Border Style (REQUIRED for data slides)

### ❌ WRONG (Generic uniform borders):
- All borders same weight and color (looks like an Excel spreadsheet)
- Thick dark borders around every cell
- Solid teal/blue cell fills
- Free-floating text boxes with numbers scattered around

### ✅ CORRECT (McKinsey hierarchical borders):
```
  Metric            Current    Target     Gap         ← Header: #F2F2F2 fill, #003A70 navy bold
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 2pt THICK navy border (signature element)
  Capacity (GW)     0.5        10.0       9.5         ← White fill, #333333 grey text, 10pt
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← 0.5pt light grey #D9D9D9 (subtle)
  Investment (€B)   1.2        15.0       13.8
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← 0.5pt light grey (subtle)
  Jobs (000s)       2.1        15.0       12.9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ← 1pt navy bottom border (clean closure)
```

**Border hierarchy** (THIS IS WHAT MAKES IT LOOK McKINSEY):
1. **Header bottom border**: 2pt navy `#003A70` — the thickest, most prominent line
2. **Table bottom border**: 1pt navy `#003A70` — provides closure
3. **Internal row separators**: 0.5pt light grey `#D9D9D9` — subtle, minimal
4. **Vertical gridlines**: NONE preferred, or 0.5pt light grey if needed
5. **Outer left/right borders**: NONE — table floats cleanly on white background

Additional table rules:
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
y=6.2"  └────────────┘  └────────────┘  └────────────┘
                                                           ← clear gap
y=6.75" Source: Government reports; McKinsey analysis      ← anchored near bottom
y=6.9"  ────────────────────────────────────────────────
y=7.0"  CONFIDENTIAL                 McKinsey & Company  1
```

**Rule**: Body content (including bottom metrics) must STOP by y=6.4". Source anchors at y=6.75".

---

## Example 7: Correct Footer Format (CRITICAL — Patronus Checked)

### ❌ WRONG — Missing McKinsey branding:
```
y=6.6"  Source: Industry reports; McKinsey analysis
y=6.9"  ────────────────────────────────────────────────
y=7.0"  CONFIDENTIAL                                  1
```
**Problem**: No "McKinsey & Company" text — automatic FAIL.

### ❌ WRONG — Source floating too high:
```
y=6.2"  Source: Industry reports; McKinsey analysis     ← Too high, wastes space
y=6.9"  ────────────────────────────────────────────────
y=7.0"  CONFIDENTIAL                 McKinsey & Company  1
```
**Problem**: Source should be anchored near the bottom at y=6.75", not floating in the middle.

### ✅ CORRECT — Complete McKinsey footer:
```
y=6.75" Source: Industry reports; McKinsey analysis     ← Anchored close to bottom
y=6.9"  ────────────────────────────────────────────────  ← Thin grey divider
y=7.0"  CONFIDENTIAL                 McKinsey & Company  1  ← Full branding
```
**All four elements present**: Source (anchored near bottom), divider line, CONFIDENTIAL, McKinsey & Company + page number.
