"""
FastAPI server for the Slide Skill OpenEnv environment.

Endpoints follow the OpenEnv HTTP protocol:
    POST /reset                    → initialize or restart a session
    POST /step                     → apply an action and return observation
    DELETE /sessions/{session_id}  → clean up a session
    GET  /health                   → liveness check

The server is stateful: environment instances are kept in memory.
Use a single Uvicorn worker (--workers 1) since LibreOffice is not
thread-safe when called concurrently from the same process.
"""

from __future__ import annotations

import logging
import traceback
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env from the repo root (one level up from openenv/)
load_dotenv(Path(__file__).parent.parent / ".env")
from typing import Annotated, Any

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Path
from pydantic import BaseModel

from models import SlideSkillAction, SlideSkillObservation
from slide_skill_environment import SlideSkillEnvironment


# Single shared environment instance. Sessions are isolated at the file
# level, so this is safe for concurrent requests.
_env: SlideSkillEnvironment | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    global _env
    _env = SlideSkillEnvironment()
    yield
    _env = None


app = FastAPI(
    title="Slide Skill OpenEnv",
    description=(
        "OpenEnv-compatible environment for optimizing McKinsey-style "
        "PowerPoint slides by evolving DESIGN_RULES.md and EXAMPLES.md."
    ),
    lifespan=lifespan,
)


class ResetRequest(BaseModel):
    session_id: str | None = None


class ResetResponse(BaseModel):
    session_id: str
    message: str


class StepRequest(BaseModel):
    session_id: str
    action: SlideSkillAction


@app.post("/reset", response_model=ResetResponse)
async def reset(
    request: ResetRequest = Body(default=ResetRequest()),
) -> ResetResponse:
    """Initialize or restart an optimization session."""
    assert _env is not None
    session_id = _env.reset(session_id=request.session_id)
    return ResetResponse(
        session_id=session_id,
        message=f"Session {session_id} initialized with baseline skill files.",
    )


@app.post("/step", response_model=SlideSkillObservation)
async def step(request: StepRequest) -> SlideSkillObservation:
    """Apply an action to the session and return the resulting observation."""
    assert _env is not None
    try:
        observation = _env.step(
            session_id=request.session_id,
            action=request.action,
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {request.session_id!r} not found. Call /reset first.",
        )
    except (RuntimeError, ValueError) as exc:
        logger.error("Step failed:\n%s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(exc))
    return observation


@app.delete("/sessions/{session_id}")
async def close_session(
    session_id: Annotated[str, Path(description="Session ID to clean up.")],
) -> dict[str, Any]:
    """Clean up session resources (deletes /tmp/ working directory)."""
    assert _env is not None
    try:
        _env.close(session_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id!r} not found.",
        )
    return {"message": f"Session {session_id} closed."}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "supports_concurrent_sessions": True}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=1)
