# Examples — Reference Slide Structures

## Example 1: Data Table Slide

**Title**: "Electrolyzer costs have fallen 62% since 2010, with alkaline technology maintaining a persistent cost advantage over PEM"

**Divider line**: Navy (`003A70`), 1.5pt, full content width at Y=1.12"

**Body content** (Table):

| Technology | 2010 Cost ($/kW) | 2015 Cost ($/kW) | 2020 Cost ($/kW) | 2023 Cost ($/kW) | CAGR |
|------------|-------------------|-------------------|-------------------|-------------------|------|
| Alkaline | 1,200 | 900 | 600 | 450 | -7.2% |
| PEM | 2,500 | 1,800 | 1,100 | 700 | -9.4% |
| SOEC | 5,000 | 4,000 | 2,800 | 2,000 | -6.8% |

- Table header: Navy fill `003A70`, white text, bold
- Body rows: Alternating white/light gray `F2F2F2`
- All text: Arial 11pt
- Positioned: Starting Y=1.35", centered horizontally

**Footer**:
- Left: *"Source: IRENA Hydrogen Cost Database 2023; BloombergNEF; McKinsey analysis"* (8pt, italic, gray)
- Right: "1" (8pt, gray)
- Separator line at Y=6.55"

---

## Example 2: Key Findings Slide

**Title**: "Three factors explain 85% of regional variation in hydrogen production costs"

**Divider line**: Navy, 1.5pt, full width

**Body content** (Table with findings):

| # | Factor | Impact on Cost | Key Evidence |
|---|--------|---------------|--------------|
| 1 | Electricity price | 45% of total variation | Correlation r=0.92 across 30 markets |
| 2 | Capacity utilization | 25% of total variation | Plants >80% utilization achieve 30% lower LCOH |
| 3 | Electrolyzer capex | 15% of total variation | Chinese equipment 40% cheaper than European |

- Clean table formatting
- Numbered rows for clarity
- Data-rich cells with specific evidence

**Footer**: Source attribution + page number

---

## Anti-Patterns (NEVER Do These)

### ✗ Dark background with bright colored text
- Always white background, dark text

### ✗ Topic-label titles
- "Market Overview" tells the reader nothing

### ✗ Timeline/process flow for data
- Use structured tables instead

### ✗ Tiny text (below 10pt) in content areas
- Minimum 10pt even in tables

### ✗ Missing footer
- Every slide needs source + page number

### ✗ Missing title divider line
- The navy line below the title is mandatory

### ✗ Elements overlapping
- Calculate positions precisely; leave gaps between zones
