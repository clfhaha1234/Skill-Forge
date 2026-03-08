# Skill Forge

A self-improving system that iteratively generates, evaluates, and optimizes PowerPoint slides using AI. Each round produces better slides by learning from visual evaluation feedback.

## How It Works

```
Round N:
  skill_vN/ --> Executor --> slide_vN.pptx --> Evaluator --> score + feedback
                                                                   |
                                                                   v
  skill_vN/ + feedback --> Optimizer --> skill_v(N+1)/
```

Three AI-driven roles collaborate in a loop:

| Role | Responsibility |
|------|---------------|
| **Executor** | Reads the skill folder and generates a PPT using pptxgenjs |
| **Evaluator** | Scores the rendered slide image across multiple dimensions |
| **Optimizer** | Uses evaluation feedback to improve the skill folder for the next round |

## The Task

A fixed task is used across all rounds so improvements are solely from skill optimization:

> Generate a 1-slide timeline PowerPoint about Dutch Hydrogen Strategy (2020-2035) in McKinsey & Company consulting style.

## Skill Folder (What Gets Optimized)

```
skill_vN/
├── DESIGN_RULES.md    # Colors, fonts, spacing rules
└── EXAMPLES.md        # Good/bad patterns (grows over rounds)
```

Starts minimal. Grows smarter each round as evaluation feedback accumulates.

## Results

Ran 5 rounds (v0 through v4). Final score: **89/100**.

| Dimension | Score (/15) |
|-----------|-------------|
| Background & Layout | 14 |
| Color Palette | 14 |
| Typography | 13 |
| Title Quality | 15 |
| Data Presentation | 12 |
| Structural Elements | 13 |
| Overall Impression | 8 (/10) |

**Verdict:** A highly professional slide that closely mirrors McKinsey's visual language with an insight-driven title, restrained color palette, and proper structural elements.

## Project Structure

```
Skill-Forge/
├── README.MD
├── package.json
├── pptx/                          # PPTX skill (executor instructions)
│   ├── SKILL.md
│   ├── pptxgenjs.md
│   ├── editing.md
│   └── scripts/                   # Office utilities (unpack, validate, thumbnail, etc.)
├── output/
│   ├── TASK_PROMPT.md             # Fixed task used every round
│   ├── reference/                 # Gold-standard reference slide images
│   ├── skill_v0/ .. skill_v5/     # Skill versions (evolving instructions)
│   ├── generate_v0.js .. v4.js    # Generated pptxgenjs scripts
│   ├── slide_v0.pptx .. v4.pptx   # Generated slides
│   ├── slide_v0.pdf .. v4.pdf     # PDF conversions
│   ├── slide_v0-1.jpg .. v4-1.jpg # Rendered slide images
│   ├── evaluator.py               # Evaluation script
│   └── evaluation_results.json    # Score progression
└── estudio_base_...pdf            # Reference document for visual style
```

## Prerequisites

- Node.js
- Python 3
- LibreOffice (`soffice`) for PDF conversion
- Poppler (`pdftoppm`) for PDF-to-image conversion

## Setup

```bash
npm install
pip install "markitdown[pptx]" Pillow
```

## License

ISC
