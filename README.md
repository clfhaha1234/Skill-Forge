# Skill Forge

An RL environment that teaches AI to generate **professional consulting-quality slides** — automatically. It uses a generate-evaluate-optimize loop where an LLM agent iteratively rewrites its own design instructions, reaching **98/100 in just 2 steps** with zero human feedback.

## Training Metrics

### Latest Run (OpenEnv + 1M Context)

```
Step 0  ████░░░░░░░░░░░░░░░░  20/100   (baseline — neon palette, layout errors)
Step 1  █████████████░░░░░░░  66/100   (white bg, table structure, wrong font)
Step 2  ███████████████████░  98/100   (near-perfect McKinsey match)
```

> **98/100** — "An exceptional slide that perfectly captures the target consulting style, with highly professional layout and formatting."

### Previous Run (Manual Loop, 7 Steps)

<details>
<summary>Click to expand</summary>

```
Step 0  ████░░░░░░░░░░░░░░░░  43/100   (baseline — dark teal, wrong style)
Step 1  ████████░░░░░░░░░░░░  63/100   (white bg, insight title)
Step 2  █████░░░░░░░░░░░░░░░  47/100   (navy border, but table overflow)
Step 3  ███████░░░░░░░░░░░░░  59/100   (pastels fail on new topic)
Step 4  ██████████████░░░░░░  74/100   (clean, but too austere)
Step 5  ██████████████░░░░░░  75/100   (horizontal-only borders)
Step 6  █████████████████░░░  86/100   (column tints added)
Step 7  ███████████████████░  97/100   (near-perfect McKinsey match)
```

</details>

### Key Improvement: 1M Context Window

The managed `pptx` skill loads ~150K tokens of documentation into context. With the default 200K window, skill files had to be truncated to ~2000 chars — starving the optimizer of design detail. Enabling the **1M context beta** (`context-1m-2025-08-07`) removed this bottleneck, allowing full skill files to pass through and cutting convergence from 7 steps to 2.

### Reward Signal

Two complementary evaluators form the reward:

| | Patronus Gate | Gemini Score |
|---|---|---|
| **Role** | Binary quality gate (PASS/FAIL) | Fine-grained scoring (0-100) |
| **Signal** | 8 verifiable criteria checks | 7-dimension visual comparison |
| **Actionability** | "Fix criterion #2: color palette" | "Score 63 — needs improvement" |
| **Cost** | Fast, filters bad slides early | Slower, runs on gate-passed slides |

## How It Works

```
┌─────────────────────────────────────────────────┐
│                  RL LOOP                         │
│                                                  │
│   DESIGN_RULES.md ──→ Generate (Claude Sonnet)   │
│        ↑                      │                  │
│        │                      ▼                  │
│   Optimize        Evaluate (Patronus + Gemini)   │
│   (Claude Opus)              │                   │
│        ↑                     │                   │
│        └─────────────────────┘                   │
└─────────────────────────────────────────────────┘
```

Three LLMs collaborate in a loop:

| Role | Model | Responsibility |
|------|-------|---------------|
| **Generator** | Claude Sonnet 4.6 | Reads skill files + pptx reference, generates PptxGenJS code |
| **Evaluator** | Gemini 3.1 Pro | Scores rendered slide against McKinsey references (0-100) |
| **Optimizer** | Claude Opus 4.6 | Reads scores + feedback, rewrites DESIGN_RULES.md |

Plus **Patronus Judge MM** as a binary quality gate with 8 McKinsey-specific criteria.

## Architecture — OpenEnv Integration

Built as an [OpenEnv](https://github.com/patronus-ai/openenv) environment:

- **State**: Current skill files (DESIGN_RULES.md) + score history
- **Action Space**: `replace_file` / `edit_section` on skill files
- **Reward**: Patronus pass/fail gate + Gemini 0-100 fine-grained score
- **Episode**: 7 steps max, terminates at score ≥ 90 or plateau

```
POST /reset  → Initialize episode with baseline skill
POST /step   → Optimize → Generate → Evaluate → return observation
```

## Project Structure

```
Skill-Forge/
├── README.md
├── pyproject.toml                # Python package config
├── package.json                  # pptxgenjs ^4.0.1
├── .env.example                  # Environment variable reference
│
├── slide_skill_env/              # OpenEnv environment package
│   ├── app.py                    # FastAPI server (OpenEnv HTTP interface)
│   ├── slide_skill_environment.py # Core environment (reset, step, close)
│   ├── generator.py              # Claude Sonnet → PptxGenJS → PPTX → JPG
│   ├── evaluator.py              # Patronus gate + Gemini scoring
│   ├── optimizer.py              # Claude Opus skill optimizer
│   ├── client.py                 # Reference client (runs full loop)
│   ├── models.py                 # Pydantic: SkillAction, SkillObservation, SkillState
│   ├── skill_manager.py          # Applies edit_section / replace_file actions
│   ├── converter.py              # PPTX → PDF → JPG via LibreOffice + poppler
│   ├── openenv.yaml              # OpenEnv manifest
│   ├── Dockerfile                # Node.js + LibreOffice + Python
│   └── requirements.txt
│
├── pptx/                         # Generic pptx skill (DO NOT MODIFY)
│   ├── SKILL.md
│   ├── pptxgenjs.md
│   └── editing.md
│
├── skill_files_baseline/         # Starting skill (v0)
│   ├── DESIGN_RULES.md
│   └── EXAMPLES.md
│
└── output/
    ├── TASK_PROMPT.md            # Fixed task prompt
    ├── reference/                # Gold-standard McKinsey slides (JPGs)
    ├── skill_v0/ .. skill_v7/    # Historical skill versions (manual loop)
    ├── episode_<uuid>/           # OpenEnv episode outputs (persistent)
    │   ├── slides/               # PPTX + PDF + JPG per step
    │   ├── skill/                # Final skill files
    │   └── skill_step_N/         # Skill snapshot at each step
    └── rl_log.md                 # Detailed iteration log
```

## Setup

```bash
# Node dependencies (pptxgenjs)
npm install

# Python dependencies
pip install -e .

# Environment variables
cp .env.example .env
# Set ANTHROPIC_API_KEY, GEMINI_API_KEY, PATRONUS_API_KEY
```

## Running

### OpenEnv Server

```bash
uvicorn slide_skill_env.app:app --host 0.0.0.0 --port 8000
```

### Reference Client (Full Loop)

```bash
python -m slide_skill_env.client --server http://localhost:8000 --max-steps 7
```

### Docker

```bash
docker build -f slide_skill_env/Dockerfile -t slide-skill-env .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e PATRONUS_API_KEY=$PATRONUS_API_KEY \
  slide-skill-env
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Claude API key (generator + optimizer) |
| `GEMINI_API_KEY` | Yes | — | Gemini API key (evaluator) |
| `PATRONUS_API_KEY` | Yes | — | Patronus API key (quality gate) |
| `SLIDE_SKILL_MAX_STEPS` | No | `7` | Steps per episode |
| `SLIDE_SKILL_SCORE_THRESHOLD` | No | `90` | Early termination score |
| `SLIDE_SKILL_PLATEAU_PATIENCE` | No | `2` | Steps without improvement before stopping |

## License

ISC
