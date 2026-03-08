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

## What Gets Optimized

There are two distinct layers of "skill files":

| Layer | Location | Purpose | Optimized? |
|-------|----------|---------|------------|
| Generic pptx tooling | `pptx/` | Teaches Claude how to use pptxgenjs (API reference, shapes, coordinates) | **No** — stable Anthropic skill |
| Brand style guidelines | `skill_vN/` or `skill_files_baseline/` | McKinsey-specific colors, typography, structural elements | **Yes** — evolves each round |

The optimizer rewrites `DESIGN_RULES.md` and `EXAMPLES.md` each round. The `pptx/` skill files are never touched.

## Results (Classical Loop)

Ran 5 rounds (v0 through v4). Final score: **89/100**.

| Dimension | Score |
|-----------|-------|
| Background & Layout | 14/15 |
| Color Palette | 14/15 |
| Typography | 13/15 |
| Title Quality | 15/15 |
| Data Presentation | 12/15 |
| Structural Elements | 13/15 |
| Overall Impression | 8/10 |

**Verdict:** A highly professional slide that closely mirrors McKinsey's visual language with an insight-driven title, restrained color palette, and proper structural elements.

## Project Structure

```
Skill-Forge/
├── README.MD
├── package.json                   # pptxgenjs ^4.0.1
├── pyproject.toml                 # Python package (OpenEnv server)
├── .env.example                   # Environment variable reference
│
├── pptx/                          # Generic pptx skill (DO NOT MODIFY)
│   ├── SKILL.md
│   ├── pptxgenjs.md
│   ├── editing.md
│   └── scripts/                   # Office utilities (unpack, validate, thumbnail)
│
├── skill_files_baseline/          # Committed minimal baseline (skill_v0 content)
│   ├── DESIGN_RULES.md            # Starting style rules (teal palette, basic typography)
│   └── EXAMPLES.md                # Empty — no prior rounds
│
├── openenv/                       # OpenEnv environment (new)
│   ├── app.py                     # FastAPI server (POST /reset, /step, DELETE /sessions)
│   ├── client.py                  # Reference client + LLM optimizer loop
│   ├── models.py                  # Pydantic models: actions, observation, state
│   ├── slide_skill_environment.py # Core environment logic (reset, step, close)
│   ├── skill_manager.py           # Applies EditSection / ReplaceFile actions
│   ├── slide_generator.py         # LLM → JS → Node → LibreOffice → JPG pipeline
│   ├── evaluator_adapter.py       # Gemini 3.1 Pro vision evaluator (reusable class)
│   ├── openenv.yaml               # OpenEnv manifest
│   └── Dockerfile                 # Node.js + LibreOffice + poppler + Python
│
└── output/
    ├── TASK_PROMPT.md             # Fixed task used every round
    ├── reference/                 # Gold-standard McKinsey reference images (JPGs)
    ├── skill_v0/ .. skill_v5/     # Historical skill versions
    ├── generate_v0.js .. v5.js    # Historical generated JS scripts
    ├── slide_v0.pptx .. v5.pptx   # Historical generated slides
    ├── evaluator.py               # Original standalone evaluator script
    └── evaluation_results.json    # Score progression
```

## Prerequisites

### Classical loop (manual)
- Node.js
- Python 3
- LibreOffice (`soffice`) for PDF conversion
- Poppler (`pdftoppm`) for PDF-to-image conversion

### OpenEnv server
All of the above, plus Python 3.12+ and the packages in `pyproject.toml`.

## Setup

```bash
# Node dependencies (pptxgenjs)
npm install

# Python dependencies
pip install -e ".[server]"

# Environment variables
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
```

## Running the OpenEnv Server

```bash
cd openenv
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
```

Then run the reference client (full optimization loop):

```bash
python openenv/client.py --server http://localhost:8000 --max-steps 7
```

Or a smoke test (single step):

```bash
python openenv/client.py --server http://localhost:8000 --smoke-test
```

## Docker

```bash
# Build
docker build -f openenv/Dockerfile -t slide-skill-openenv .

# Run
docker run -p 8000:8000 -e GEMINI_API_KEY=$GEMINI_API_KEY slide-skill-openenv
```

> **Note:** The Docker image is ~600-700 MB due to LibreOffice (~500 MB). LibreOffice is required for `.pptx → .pdf` conversion and has no lighter alternative that faithfully renders pptxgenjs output.

## OpenEnv Action Space

The agent can submit two types of actions each step:

**`replace_file`** — Rewrite an entire skill file (matches how the historical optimizer works):
```json
{
  "action_type": "replace_file",
  "file": "DESIGN_RULES.md",
  "new_content": "# Design Rules\n\n## Color Palette\n- Navy (#0C2340)..."
}
```

**`edit_section`** — Surgically update one markdown section:
```json
{
  "action_type": "edit_section",
  "file": "DESIGN_RULES.md",
  "section_heading": "Color Palette",
  "new_body": "- Navy (#0C2340): primary\n- White: background\n"
}
```

## Observation Space

Each step returns:

| Field | Type | Description |
|-------|------|-------------|
| `scores.background_layout` | int 0–15 | White bg, margins, layout |
| `scores.color_palette` | int 0–15 | Navy/white/grey restraint |
| `scores.typography` | int 0–15 | Font hierarchy, serif title |
| `scores.title_quality` | int 0–15 | "So-what" insight title |
| `scores.data_presentation` | int 0–15 | Structured table format |
| `scores.structural_elements` | int 0–15 | Divider line, footer, footnotes |
| `scores.overall_impression` | int 0–10 | Holistic McKinsey feel |
| `total` | int 0–100 | Sum of all scores |
| `strengths` | list[str] | What the slide does well |
| `weaknesses` | list[str] | What to improve |
| `one_line_verdict` | str | Evaluator summary |
| `reward` | float –0.3…+0.3 | Capped score delta / 100 |
| `done` | bool | True when max_steps reached |
| `design_rules_content` | str | Current DESIGN_RULES.md |
| `examples_content` | str | Current EXAMPLES.md |

## Environment Variables

See `.env.example` for the full reference.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | — | Gemini API key — generator (Flash), evaluator + optimizer (Pro) |
| `SLIDE_SKILL_MAX_STEPS` | No | `7` | Steps per episode (~60-120s each) |

## License

ISC
