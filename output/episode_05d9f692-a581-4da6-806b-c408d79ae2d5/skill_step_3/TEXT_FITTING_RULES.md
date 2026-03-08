# Text Fitting & Overflow Prevention Rules — CRITICAL

## THE #1 FORMATTING RULE: NO TEXT TRUNCATION, EVER
Text truncation (e.g., "National Hydrog..." or "10 GW target reac...") is the single most damaging formatting error. It makes a slide unpresentable. Every piece of text MUST be fully visible.

## Mandatory Text Fitting Strategies

### 1. Size Boxes to Fit Content (NOT content to fit boxes)
- **ALWAYS calculate the text length FIRST**, then size the container to fit
- If a box contains "National Hydrogen Strategy 2025", the box must be wide enough (and tall enough) to display the ENTIRE string
- NEVER set a fixed small box size and then try to cram text into it
- When in doubt, make boxes WIDER and TALLER than you think necessary

### 2. Use Abbreviations and Short Labels When Space is Tight
- If the layout requires small boxes (e.g., a timeline with many phases), use SHORT labels:
  - ❌ "National Hydrogen Strategy Phase 1" → gets truncated
  - ✅ "Nat'l H₂ Strategy P1" or just "Phase 1: H₂ Strategy"
- Prefer 2–4 word labels inside small boxes; put the full description in a subtitle or annotation BELOW the box
- Split into: **short label inside box** + **full description outside/below**

### 3. Font Size Reduction for Constrained Spaces
- Timeline boxes and small containers: use **9–10pt** font, NOT 11–14pt
- Box labels: **9–11pt** is acceptable for readability in small containers
- Never go below 8pt for any visible text
- Reduce font size BEFORE truncating text

### 4. Multi-line Wrapping Over Truncation
- If text doesn't fit on one line, WRAP it to 2–3 lines within the box
- Increase box HEIGHT to accommodate wrapped text
- Set text box `word_wrap = True` and `auto_size = None` (do NOT auto-shrink or clip)
- NEVER clip or truncate — always allow wrapping

### 5. Minimum Box Dimensions
- Any box containing text must be at minimum:
  - **Width**: 1.2 inches (for short labels) to 2.5 inches (for descriptions)
  - **Height**: 0.5 inches (single line) to 1.0 inches (multi-line)
- Timeline phase boxes specifically: minimum 1.5" wide × 0.7" tall
- If you have more than 4–5 boxes in a horizontal row, consider stacking into 2 rows or using a vertical layout instead

### 6. Horizontal Space Budget
- Standard slide is 10" wide with 0.5" margins = **9" usable width**
- For a timeline with N phases side by side: each phase gets at most `(9 - gaps) / N` inches
- If N > 5, each box is under 1.5" — you MUST use short labels or switch to a vertical/stacked layout
- Always subtract gap space (0.1–0.2" between boxes) from the budget

## Icon and Text Overlap Prevention
- **NEVER place icons and text in the same bounding box** without explicit padding
- If icons are used in timeline bars or boxes:
  - Place the icon ABOVE or to the LEFT of the text, not overlapping
  - Add at least 0.2" padding between icon edge and text start
  - Or: skip icons entirely and use text-only labels (preferred for McKinsey style)
- **McKinsey style preference: NO icons in timeline boxes.** Use clean text labels only.

## Title-Specific Overflow Rules
- Title font: **18–22pt** (NOT 24–28pt — larger sizes cause overflow on insight titles)
- Maximum title length: **120 characters** (roughly 1.5 lines at 20pt on a 9" wide area)
- If the insight title exceeds 120 characters, shorten it — do NOT wrap to 3+ lines
- Title text box width: **8.5–9.0 inches** (use nearly full slide width)
- Title MUST NOT extend vertically past y=1.1" on the slide
- The divider line sits at y=1.2" — title must end ABOVE this line
- Leave at least **0.1" gap** between the bottom of the title text and the divider line

## Source & Footer Overlap Prevention
- The source text and footer occupy the **bottom 0.75" of the slide** (from y=6.75" to y=7.5")
- Reserved vertical zones (standardized positions):
  - **y = 6.4"**: Hard stop for body content (nothing below this)
  - **y = 6.75"**: Source text starts here ("Source: ...") — anchored near bottom
  - **y = 6.9"**: Footer divider line
  - **y = 7.0"**: Footer text (CONFIDENTIAL + McKinsey & Company + page number)
  - **y = 7.5"**: Slide bottom edge
- **Body content (including bottom metrics/callouts) must NOT extend below y=6.4"**
- **Source text must be at y=6.75"** — anchored close to the footer, NOT floating high
- There must be at least 0.15" clear gap between the lowest body element and the source text

## Python-PPTX Specific Tips
When generating slides programmatically:
- Set `txBody` properties: `wrap="square"` to enable word wrapping
- Do NOT set `autofit` to shrink text — it causes unpredictable sizing
- Set explicit shape dimensions (`width`, `height`) large enough for content
- For text frames: set `word_wrap = True`
- For auto-sizing: use `MSO_AUTO_SIZE.NONE` (manual sizing) rather than `MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT` which can cause layout shifts
- Calculate approximate text width: ~0.1" per character at 10pt, ~0.12" per character at 12pt
- Always add 0.2" padding to calculated minimum width

## Pre-Render Checklist for Text Fitting
Before finalizing any element:
- [ ] Every text string is fully visible — no "..." or cutoff words
- [ ] All boxes are wide and tall enough for their content
- [ ] No two text elements overlap each other
- [ ] Icons do not overlap with adjacent text
- [ ] Title does not touch or cross the divider line (title ends above y=1.1", line at y=1.2")
- [ ] Source text is anchored at y=6.75" (near bottom, not floating high)
- [ ] Source text does not touch or overlap body content above it
- [ ] Footer text does not overlap source text
- [ ] Footer includes "McKinsey & Company" branding in the bottom-right
- [ ] Font sizes are appropriate for container sizes (smaller containers = smaller font)
