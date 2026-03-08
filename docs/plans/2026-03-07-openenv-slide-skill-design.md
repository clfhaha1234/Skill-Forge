# Design: Self-Improving PPT Skill in OpenEnv

**Date:** 2026-03-07
**Status:** Approved

## Goal

Build an OpenEnv environment that automatically optimizes a PPT generation skill based on user-provided reference slides. Each step runs a full optimize→generate→evaluate cycle, producing progressively better slides.

## Three LLM Roles

| Role | Model | Purpose |
|------|-------|---------|
| Optimizer | Claude Opus 4.6 | Agentic editor — modifies skill folder (edit/add/delete files) based on feedback |
| Executor | Claude Sonnet 4.6 + managed pptx skill | Generates slides using the skill folder as context |
| Evaluator | Gemini 3.1 Pro Preview | Vision-based scoring against user reference images |

## Environment API

```python
class SlideSkillEnvironment(Environment):

    async def reset(self, config):
        """
        config:
          - reference_images: list[bytes]   # gold-standard slide images
          - task_prompt: str                # what slide to generate
          - baseline_skill: str | None      # initial DESIGN_RULES.md (optional)
          - max_steps: int                  # default 7
          - score_threshold: int            # default 90
          - plateau_patience: int           # default 2

        Returns: Observation with baseline score
        """

    async def step(self, action):
        """
        action:
          - hint: str | None   # optional guidance for optimizer

        Runs: optimize → generate → convert → evaluate → check done
        Returns: StepResult(observation, reward, done)
        """

    async def close(self):
        """Cleanup temp files"""
```

## Data Models

```python
class SkillAction(Action):
    hint: str | None = None

class SkillObservation(Observation):
    step_number: int
    scores: dict                    # 7 dimensions
    total: int                      # 0-100
    reward: float                   # score delta, capped
    strengths: list[str]
    weaknesses: list[str]
    one_line_verdict: str
    skill_files: dict[str, str]     # filename → content
    slide_image_base64: str         # rendered slide JPG
    done: bool
    done_reason: str | None         # "threshold", "plateau", "max_steps"

class SkillState(State):
    episode_id: str
    step_count: int
    score_history: list[int]
    best_score: int
    best_skill_files: dict[str, str]
```

## Internal Flow of step()

```
step(action: SkillAction)
│
├── 1. OPTIMIZE (Claude Opus 4.6 + tool use)
│   │  Multi-turn agent loop with file tools:
│   │    read_file, write_file, delete_file, list_files
│   │  Reads: previous feedback, reference images, current skill, hint
│   │  Produces: updated skill folder on disk
│   │  Typically 3-10 tool calls per round
│   │
├── 2. GENERATE (Claude Sonnet 4.6 + managed pptx skill)
│   │  Single API call with code_execution tool
│   │  Reads skill folder as message context
│   │  Produces: .pptx file (downloaded via Files API)
│   │
├── 3. CONVERT (local, no LLM)
│   │  soffice → .pdf → pdftoppm → .jpg
│   │
├── 4. EVALUATE (Gemini 3.1 Pro Preview, vision)
│   │  Slide image + reference images + scoring rubric
│   │  Returns: scores (7 dimensions) + feedback
│   │
└── 5. CHECK DONE
    │  score >= threshold? → done
    │  no improvement for N steps? → done
    │  step_count >= max_steps? → done
```

## Done Conditions

- Score >= `score_threshold` (default 90)
- No improvement for `plateau_patience` consecutive steps (default 2)
- Step count >= `max_steps` (default 7)
- Whichever comes first

## File Structure

```
openenv/
├── __init__.py
├── app.py                      # FastAPI server
├── models.py                   # SkillAction, SkillObservation, SkillState
├── slide_skill_environment.py  # SlideSkillEnvironment
├── optimizer.py                # Opus 4.6 agent loop with file tools
├── generator.py                # Sonnet 4.6 + pptx skill + Files API
├── evaluator.py                # Gemini 3.1 Pro Preview vision scoring
├── converter.py                # soffice → pdf → pdftoppm → jpg
├── skill_manager.py            # Read/write/list/delete skill folder files
├── openenv.yaml                # OpenEnv manifest
├── Dockerfile                  # Node.js + LibreOffice + poppler + Python
└── requirements.txt

skill_files_baseline/           # Committed starting point (v0 content)
├── DESIGN_RULES.md
└── EXAMPLES.md
```

Runtime temp directories (per episode):

```
/tmp/episodes/{episode_id}/
├── skill/          # Working copy (optimizer edits this)
├── slides/         # Generated slides per step
└── references/     # User-provided reference images
```

## Docker

```dockerfile
FROM python:3.12-slim
# Node.js 20 (pptxgenjs), LibreOffice (pptx→pdf), Poppler (pdf→jpg)
# Image size: ~700-800MB due to LibreOffice
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| ANTHROPIC_API_KEY | Yes | — | Opus optimizer + Sonnet generator |
| GEMINI_API_KEY | Yes | — | Gemini 3.1 Pro Preview evaluator |
| SLIDE_SKILL_MAX_STEPS | No | 7 | Max steps per episode |
| SLIDE_SKILL_SCORE_THRESHOLD | No | 90 | Score to stop at |
| SLIDE_SKILL_PLATEAU_PATIENCE | No | 2 | Rounds without improvement to stop |

## Python Dependencies

- anthropic — Opus + Sonnet API calls
- google-genai — Gemini evaluator
- fastapi + uvicorn — OpenEnv server
- openenv-core — OpenEnv framework
- pydantic — data models

## Client Usage

```python
async with SlideSkillEnv(base_url="http://localhost:8000") as env:
    obs = await env.reset({
        "reference_images": [open("ref-01.jpg", "rb").read(), ...],
        "task_prompt": "Generate a timeline slide about Dutch Hydrogen Strategy",
    })
    while not obs.done:
        obs = await env.step(SkillAction(hint=None))
        print(f"Step {obs.step_number}: {obs.total}/100")
```

## Timing

Each `step()`: ~60-120 seconds
- Opus optimizer agent: ~30-60s
- Sonnet generation: ~15-30s
- Conversion: ~5s
- Gemini evaluation: ~10-15s

## Architecture Decision: Approach A (Single Environment)

Chose single `SlideSkillEnvironment` class over microservice adapters or multi-environment composition. Internal logic split into separate modules for readability, but not separate environments.
