"""
FastAPI server for the Slide Skill OpenEnv environment.

OpenEnv API:
    POST /reset                    → initialize or restart a session
    POST /step                     → apply an action and return observation
    DELETE /sessions/{session_id}  → clean up a session
    GET  /health                   → liveness check

UI API (polling pattern — avoids proxy timeouts):
    GET  /                         → homepage
    POST /ui/generate              → enqueue a generation job, returns {job_id} immediately
    GET  /ui/status/{job_id}       → poll for job status / result
    GET  /ui/preview/{session_id}  → slide preview JPG
    GET  /ui/download/{session_id} → download the .pptx file
"""

from __future__ import annotations

import asyncio
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path as FilePath
from typing import Annotated, Any

from dotenv import load_dotenv
from loguru import logger

# Route stdlib logging through loguru so all dependencies show up consistently.
import logging as _stdlib_logging
_stdlib_logging.basicConfig(handlers=[], level=_stdlib_logging.WARNING)

class _InterceptHandler(_stdlib_logging.Handler):
    def emit(self, record: _stdlib_logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno  # type: ignore[assignment]
        frame, depth = _stdlib_logging.currentframe(), 2
        while frame and frame.f_code.co_filename == _stdlib_logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

_stdlib_logging.root.handlers = [_InterceptHandler()]
_stdlib_logging.root.setLevel(_stdlib_logging.DEBUG)
logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")

# Load .env from repo root (one level up from openenv/)
load_dotenv(FilePath(__file__).parent.parent / ".env")

import uvicorn
from fastapi import Body, FastAPI, HTTPException
from fastapi import Path as FAPIPath
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

from models import SlideSkillAction, SlideSkillObservation
from slide_skill_environment import SlideSkillEnvironment

# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

_env: SlideSkillEnvironment | None = None

# UI slides: session_id → {jpg: Path, pptx: Path}
_ui_slides: dict[str, dict[str, FilePath]] = {}

# Jobs: job_id → {status: pending|running|done|error, result|error}
_jobs: dict[str, dict[str, Any]] = {}

# Only one LibreOffice conversion at a time
_generation_lock = asyncio.Semaphore(1)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    global _env
    logger.info("Initialising SlideSkillEnvironment…")
    try:
        _env = SlideSkillEnvironment()
        logger.info("Environment ready.")
    except Exception:
        logger.exception("Failed to initialise environment — server will start but generation will not work")
    yield
    _env = None


app = FastAPI(
    title="Slide Skill OpenEnv",
    description="OpenEnv environment for optimising professional PowerPoint slide generation.",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Slide Forge — AI Slide Generator</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: #f0f2f5; color: #1a1a2e; min-height: 100vh;
  }
  header {
    background: #0C2340; color: #fff;
    padding: 20px 40px; display: flex; align-items: center; gap: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,.3);
  }
  header .logo { font-size: 28px; }
  header h1 { font-size: 20px; font-weight: 700; letter-spacing: -.3px; }
  header p  { font-size: 13px; opacity: .65; margin-top: 2px; }
  .main { max-width: 820px; margin: 48px auto; padding: 0 20px; }
  .card {
    background: #fff; border-radius: 12px; padding: 36px 40px;
    box-shadow: 0 2px 16px rgba(0,0,0,.08);
  }
  .card h2 { font-size: 17px; font-weight: 600; margin-bottom: 8px; color: #0C2340; }
  .card p.hint { font-size: 13px; color: #6b7280; margin-bottom: 20px; line-height: 1.5; }
  textarea {
    width: 100%; height: 130px; border: 1.5px solid #d1d5db; border-radius: 8px;
    padding: 14px 16px; font-size: 14px; font-family: inherit; resize: vertical;
    outline: none; transition: border-color .2s; color: #111827; line-height: 1.6;
  }
  textarea:focus { border-color: #0C2340; }
  .btn {
    margin-top: 16px; background: #0C2340; color: #fff; border: none; border-radius: 8px;
    padding: 12px 28px; font-size: 15px; font-weight: 600; cursor: pointer;
    transition: background .2s, transform .1s; display: inline-flex; align-items: center; gap: 8px;
  }
  .btn:hover:not(:disabled) { background: #163d6e; }
  .btn:active:not(:disabled) { transform: scale(.98); }
  .btn:disabled { opacity: .5; cursor: not-allowed; }
  #status { margin-top: 28px; display: none; }
  .progress-bar-wrap { height: 6px; background: #e5e7eb; border-radius: 3px; overflow: hidden; margin-bottom: 10px; }
  .progress-bar {
    height: 100%; background: #0C2340; border-radius: 3px;
    animation: indeterminate 1.8s ease-in-out infinite;
  }
  @keyframes indeterminate {
    0%   { margin-left: 0; width: 30%; }
    50%  { margin-left: 40%; width: 40%; }
    100% { margin-left: 100%; width: 0; }
  }
  .status-text { font-size: 13px; color: #6b7280; }
  #result { margin-top: 32px; display: none; }
  .result-grid { display: flex; gap: 28px; align-items: flex-start; flex-wrap: wrap; }
  .slide-preview {
    flex: 1; min-width: 260px; border: 1px solid #e5e7eb; border-radius: 8px;
    overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,.10);
  }
  .slide-preview img { width: 100%; display: block; }
  .result-meta { flex: 0 0 220px; }
  .score-badge {
    background: #0C2340; color: #fff; border-radius: 8px; padding: 16px 20px; margin-bottom: 16px;
  }
  .score-badge .score-num { font-size: 36px; font-weight: 700; line-height: 1; }
  .score-badge .score-label { font-size: 12px; opacity: .7; margin-top: 2px; }
  .verdict { font-size: 13px; color: #374151; line-height: 1.5; margin-bottom: 20px; font-style: italic; }
  .download-btn {
    display: block; width: 100%; background: #c8102e; color: #fff; border: none;
    border-radius: 8px; padding: 12px 0; font-size: 14px; font-weight: 600;
    cursor: pointer; text-align: center; text-decoration: none; transition: background .2s;
  }
  .download-btn:hover { background: #a00d25; }
  .error-box {
    background: #fef2f2; border: 1px solid #fca5a5; border-radius: 8px;
    padding: 14px 18px; color: #b91c1c; font-size: 13px; line-height: 1.5;
    margin-top: 24px; display: none;
  }
  .divider { height: 1px; background: #e5e7eb; margin: 8px 0 20px; }
  .api-note { margin-top: 28px; font-size: 12px; color: #9ca3af; text-align: center; }
  .api-note a { color: #6b7280; }
</style>
</head>
<body>
<header>
  <span class="logo">📊</span>
  <div>
    <h1>Slide Forge</h1>
    <p>AI-powered professional PowerPoint generator</p>
  </div>
</header>

<div class="main">
  <div class="card">
    <h2>Generate a slide</h2>
    <p class="hint">
      Describe the slide you want. The AI will generate a professional
      PowerPoint using the optimised skill files — then render it as a downloadable .pptx.
      <br>Generation takes around <strong>60–90 seconds</strong>.
    </p>
    <div class="divider"></div>

    <textarea id="prompt" placeholder="e.g. A 1-slide comparison of Grey, Blue, and Green hydrogen production methods, with a structured table and insight-driven title."></textarea>

    <button class="btn" id="generateBtn" onclick="generate()">
      <span>✦</span> Generate slide
    </button>

    <div id="status">
      <div class="progress-bar-wrap"><div class="progress-bar"></div></div>
      <span class="status-text" id="statusText">Starting…</span>
    </div>

    <div class="error-box" id="errorBox"></div>

    <div id="result">
      <div class="result-grid">
        <div class="slide-preview">
          <img id="previewImg" src="" alt="Generated slide preview">
        </div>
        <div class="result-meta">
          <div class="score-badge">
            <div class="score-num" id="scoreNum">—</div>
            <div class="score-label">/ 100 quality score</div>
          </div>
          <p class="verdict" id="verdictText"></p>
          <a class="download-btn" id="downloadBtn" href="#" download="slide.pptx">
            ⬇ Download .pptx
          </a>
        </div>
      </div>
    </div>
  </div>

  <p class="api-note">
    OpenEnv API at <a href="/docs">/docs</a> &nbsp;·&nbsp; <a href="/health">/health</a>
  </p>
</div>

<script>
let _pollTimer = null;

function showError(msg) {
  document.getElementById('status').style.display = 'none';
  const box = document.getElementById('errorBox');
  box.textContent = '⚠ ' + msg;
  box.style.display = 'block';
  document.getElementById('generateBtn').disabled = false;
}

function showResult(data) {
  document.getElementById('status').style.display = 'none';
  document.getElementById('scoreNum').textContent = data.score ?? '—';
  document.getElementById('verdictText').textContent = data.verdict ?? '';
  document.getElementById('previewImg').src = '/ui/preview/' + data.session_id + '?t=' + Date.now();
  document.getElementById('downloadBtn').href = '/ui/download/' + data.session_id;
  document.getElementById('result').style.display = 'block';
  document.getElementById('generateBtn').disabled = false;
}

async function poll(jobId, elapsed) {
  try {
    const resp = await fetch('/ui/status/' + jobId);
    if (!resp.ok) { showError('Status check failed: ' + resp.statusText); return; }
    const job = await resp.json();

    if (job.status === 'done') {
      showResult(job.result);
    } else if (job.status === 'error') {
      showError(job.error || 'Generation failed.');
    } else {
      // still running — update elapsed time and poll again in 3s
      const mins = Math.floor(elapsed / 60), secs = elapsed % 60;
      const timeStr = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
      document.getElementById('statusText').textContent =
        `Generating slide… (${timeStr} elapsed)`;
      _pollTimer = setTimeout(() => poll(jobId, elapsed + 3), 3000);
    }
  } catch (err) {
    showError('Network error while polling: ' + err.message);
  }
}

async function generate() {
  const prompt = document.getElementById('prompt').value.trim();
  if (!prompt) { alert('Please enter a slide description.'); return; }

  if (_pollTimer) { clearTimeout(_pollTimer); _pollTimer = null; }

  document.getElementById('generateBtn').disabled = true;
  document.getElementById('result').style.display = 'none';
  document.getElementById('errorBox').style.display = 'none';
  document.getElementById('status').style.display = 'block';
  document.getElementById('statusText').textContent = 'Queuing job…';

  try {
    const resp = await fetch('/ui/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({prompt}),
    });
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({detail: resp.statusText}));
      showError(err.detail || resp.statusText);
      return;
    }
    const {job_id} = await resp.json();
    document.getElementById('statusText').textContent = 'Generating slide… (0s elapsed)';
    poll(job_id, 3);
  } catch (err) {
    showError(err.message);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('prompt').addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) generate();
  });
});
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def homepage() -> HTMLResponse:
    return HTMLResponse(content=_HTML)


# ---------------------------------------------------------------------------
# UI generation — non-blocking job pattern
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    prompt: str


@app.post("/ui/generate")
async def ui_generate(request: GenerateRequest) -> JSONResponse:
    """Enqueue a generation job. Returns {job_id} immediately; poll /ui/status/{job_id}."""
    if _env is None:
        raise HTTPException(status_code=503, detail="Environment not initialised.")
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt must not be empty")

    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "pending", "result": None, "error": None}
    logger.info(f"Job {job_id[:8]} enqueued | prompt: {request.prompt[:60]!r}")

    asyncio.create_task(_run_generation_task(job_id, request.prompt.strip()))
    return JSONResponse({"job_id": job_id})


async def _run_generation_task(job_id: str, prompt: str) -> None:
    """Background task: acquire lock, run blocking generation in thread, update job state."""
    _jobs[job_id]["status"] = "running"
    logger.info(f"Job {job_id[:8]} started")
    loop = asyncio.get_running_loop()
    try:
        async with _generation_lock:
            score, verdict, session_id = await loop.run_in_executor(
                None, _run_generation_sync, prompt
            )
        _jobs[job_id] = {
            "status": "done",
            "result": {"session_id": session_id, "score": score, "verdict": verdict},
            "error": None,
        }
        logger.info(f"Job {job_id[:8]} done | score={score} | {verdict}")
    except Exception as exc:
        logger.exception(f"Job {job_id[:8]} failed: {exc}")
        _jobs[job_id] = {"status": "error", "result": None, "error": str(exc)}


def _run_generation_sync(prompt: str) -> tuple[int, str, str]:
    """Blocking helper: reset session, generate slide, evaluate."""
    assert _env is not None
    session_id = _env.reset()
    state = _env._sessions[session_id]
    session_dir = FilePath(state.session_dir)

    logger.info(f"Generating JS + PPTX for session {session_id[:8]}…")
    jpg_path = _env._generator.generate(
        session_id=session_id,
        session_dir=session_dir,
        state=state,
        task_prompt_override=prompt,
    )
    pptx_path = session_dir / "output" / "slide.pptx"

    logger.info(f"Evaluating slide for session {session_id[:8]}…")
    eval_result = _env._evaluator.evaluate(jpg_path)
    score: int = eval_result.get("total", 0)
    verdict: str = eval_result.get("one_line_verdict", "")

    _ui_slides[session_id] = {"jpg": jpg_path, "pptx": pptx_path}
    return score, verdict, session_id


@app.get("/ui/status/{job_id}")
async def ui_status(
    job_id: Annotated[str, FAPIPath(description="Job ID from /ui/generate")],
) -> JSONResponse:
    """Poll for job status. Returns {status, result, error}."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return JSONResponse(job)


@app.get("/ui/preview/{session_id}")
async def ui_preview(
    session_id: Annotated[str, FAPIPath(description="Session ID from job result")],
) -> FileResponse:
    """Return the generated slide as a JPEG for preview."""
    entry = _ui_slides.get(session_id)
    if not entry or not entry["jpg"].exists():
        raise HTTPException(status_code=404, detail="Preview not found.")
    return FileResponse(entry["jpg"], media_type="image/jpeg")


@app.get("/ui/download/{session_id}")
async def ui_download(
    session_id: Annotated[str, FAPIPath(description="Session ID from job result")],
) -> FileResponse:
    """Download the generated .pptx file."""
    entry = _ui_slides.get(session_id)
    if not entry or not entry["pptx"].exists():
        raise HTTPException(status_code=404, detail="Slide file not found.")
    return FileResponse(
        entry["pptx"],
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="slide.pptx",
        headers={"Content-Disposition": "attachment; filename=slide.pptx"},
    )


# ---------------------------------------------------------------------------
# OpenEnv API
# ---------------------------------------------------------------------------

class ResetRequest(BaseModel):
    session_id: str | None = None

class ResetResponse(BaseModel):
    session_id: str
    message: str

class StepRequest(BaseModel):
    session_id: str
    action: SlideSkillAction


@app.post("/reset", response_model=ResetResponse)
async def reset(request: ResetRequest = Body(default=ResetRequest())) -> ResetResponse:
    assert _env is not None
    session_id = _env.reset(session_id=request.session_id)
    return ResetResponse(
        session_id=session_id,
        message=f"Session {session_id} initialized with baseline skill files.",
    )


@app.post("/step", response_model=SlideSkillObservation)
async def step(request: StepRequest) -> SlideSkillObservation:
    assert _env is not None
    try:
        observation = _env.step(session_id=request.session_id, action=request.action)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {request.session_id!r} not found. Call /reset first.",
        )
    except (RuntimeError, ValueError) as exc:
        logger.exception(f"Step failed for session {request.session_id!r}")
        raise HTTPException(status_code=500, detail=str(exc))
    return observation


@app.delete("/sessions/{session_id}")
async def close_session(
    session_id: Annotated[str, FAPIPath(description="Session ID to clean up.")],
) -> dict[str, Any]:
    assert _env is not None
    _ui_slides.pop(session_id, None)
    try:
        _env.close(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Session {session_id!r} not found.")
    return {"message": f"Session {session_id} closed."}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "supports_concurrent_sessions": True}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
