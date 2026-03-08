"""
Reference client for the Slide Skill OpenEnv server.

Demonstrates how an optimizer agent would interact with the environment:
    1. Reset to get a session ID.
    2. Submit the baseline action (no-op replace to trigger generation).
    3. Call the LLM optimizer using the observation feedback.
    4. Submit the improved DESIGN_RULES.md as a ReplaceFileAction.
    5. Repeat until done=True.

This client is also useful for smoke-testing the server without a full agent.

Usage:
    # Smoke test (single step, no optimizer LLM):
    python client.py --smoke-test

    # Full optimization loop:
    python client.py --server http://localhost:8000 --max-steps 7
"""

from __future__ import annotations

import argparse
import os
import textwrap
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).parent.parent / ".env")
from google.genai import types
import httpx
from loguru import logger

from models import SlideSkillObservation

SERVER_URL = "http://localhost:8000"
OPTIMIZER_MODEL = "gemini-3.1-pro-preview"

BASELINE_EXAMPLES_CONTENT = "(Empty — no prior optimization rounds)\n"


class SlideSkillClient:
    """HTTP client for the Slide Skill OpenEnv server."""

    def __init__(self, base_url: str = SERVER_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(timeout=300.0)  # long timeout for pipeline stages

    def reset(self, session_id: str | None = None) -> str:
        """Start a new session. Returns the session_id."""
        payload: dict[str, Any] = {}
        if session_id:
            payload["session_id"] = session_id
        resp = self._http.post(f"{self.base_url}/reset", json=payload)
        resp.raise_for_status()
        return resp.json()["session_id"]

    def step(self, session_id: str, action: dict[str, Any]) -> SlideSkillObservation:
        """
        Apply an action and return the observation.

        Args:
            session_id: Active session ID.
            action: Dict matching EditSectionAction or ReplaceFileAction schema.
                    Must include "action_type" key.
        """
        payload = {"session_id": session_id, "action": action}
        resp = self._http.post(f"{self.base_url}/step", json=payload)
        if not resp.is_success:
            raise RuntimeError(
                f"Step failed ({resp.status_code}): {resp.text}"
            )
        return SlideSkillObservation.model_validate(resp.json())

    def close(self, session_id: str) -> None:
        """Clean up the session."""
        resp = self._http.delete(f"{self.base_url}/sessions/{session_id}")
        resp.raise_for_status()

    def __enter__(self) -> SlideSkillClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self._http.close()


# ---------------------------------------------------------------------------
# Optimizer agent (reference implementation)
# ---------------------------------------------------------------------------


def call_optimizer_llm(
    obs: SlideSkillObservation,
    gemini_client: genai.Client,
) -> dict[str, Any]:
    """
    Call the optimizer LLM to generate a new DESIGN_RULES.md based on
    the evaluation feedback.

    Returns a dict suitable for the step() action parameter.
    Uses ReplaceFileAction since the historical optimizer rewrites
    the file wholesale.
    """
    prompt = textwrap.dedent(f"""\
        You are a McKinsey slide design optimizer. You are improving a
        PowerPoint generation skill by rewriting its DESIGN_RULES.md file.

        ## Current Score: {obs.total}/100

        ## Score Breakdown
        - background_layout: {obs.scores.background_layout}/15
        - color_palette: {obs.scores.color_palette}/15
        - typography: {obs.scores.typography}/15
        - title_quality: {obs.scores.title_quality}/15
        - data_presentation: {obs.scores.data_presentation}/15
        - structural_elements: {obs.scores.structural_elements}/15
        - overall_impression: {obs.scores.overall_impression}/10

        ## Evaluator Feedback
        Strengths:
        {chr(10).join(f'- {s}' for s in obs.strengths)}

        Weaknesses:
        {chr(10).join(f'- {w}' for w in obs.weaknesses)}

        Verdict: {obs.one_line_verdict}

        ## Current DESIGN_RULES.md
        {obs.design_rules_content}

        ## Current EXAMPLES.md
        {obs.examples_content}

        Your task:
        Write an improved DESIGN_RULES.md that addresses the weaknesses above
        while preserving what works well. Focus on the dimensions with the
        lowest scores. Output ONLY the markdown file content — no explanation,
        no code fences.
    """)

    response = gemini_client.models.generate_content(
        model=OPTIMIZER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=4096),
    )

    new_content = response.text.strip()

    return {
        "action_type": "replace_file",
        "file": "DESIGN_RULES.md",
        "new_content": new_content,
    }


def run_optimization_loop(server_url: str = SERVER_URL, max_steps: int = 7) -> None:
    """
    Run a full optimization episode using the LLM optimizer.

    This mirrors the historical Skill Forge loop but driven through the
    OpenEnv HTTP interface.
    """
    gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    with SlideSkillClient(base_url=server_url) as client:
        logger.info(f"Starting optimization loop (max {max_steps} steps) | server={server_url}")
        session_id = client.reset()
        logger.info(f"Session: {session_id}")

        # Step 0: baseline — generate slide with unmodified skill files.
        logger.info("Step 0/baseline | generating slide (Flash)...")
        logger.info("Step 0/baseline | running Node.js + LibreOffice → JPG...")
        logger.info("Step 0/baseline | evaluating slide (Pro)...")
        obs = client.step(
            session_id,
            {
                "action_type": "replace_file",
                "file": "EXAMPLES.md",
                "new_content": BASELINE_EXAMPLES_CONTENT,
            },
        )
        logger.info(f"Step 0/baseline | score={obs.total}/100 — {obs.one_line_verdict}")

        for step_idx in range(1, max_steps + 1):
            if obs.done:
                logger.info("Episode complete (max_steps reached).")
                break

            logger.info(f"Step {step_idx}/{max_steps} | optimizing skill files (Pro)...")
            action = call_optimizer_llm(obs, gemini_client)
            logger.info(f"Step {step_idx}/{max_steps} | generating slide (Flash)...")
            logger.info(f"Step {step_idx}/{max_steps} | running Node.js + LibreOffice → JPG...")
            logger.info(f"Step {step_idx}/{max_steps} | evaluating slide (Pro)...")
            obs = client.step(session_id, action)

            delta_str = f"{obs.reward * 100:+.0f} pts"
            logger.info(f"Step {step_idx}/{max_steps} | score={obs.total}/100 ({delta_str}) — {obs.one_line_verdict}")
            if obs.weaknesses:
                logger.info(f"Step {step_idx}/{max_steps} | top weakness: {obs.weaknesses[0]}")

        client.close(session_id)
        logger.success(f"Done. Final score: {obs.total}/100")


def smoke_test(server_url: str = SERVER_URL) -> None:
    """Run a single reset + step to verify the server is working."""
    with SlideSkillClient(base_url=server_url) as client:
        logger.info("Smoke test: resetting session...")
        session_id = client.reset()
        logger.info(f"Smoke test: session_id={session_id}")

        logger.info("Smoke test: submitting baseline action (full pipeline)...")
        obs = client.step(
            session_id,
            {
                "action_type": "replace_file",
                "file": "EXAMPLES.md",
                "new_content": BASELINE_EXAMPLES_CONTENT,
            },
        )
        logger.info(f"Smoke test: score={obs.total}/100 reward={obs.reward:+.3f} done={obs.done}")
        logger.info(f"Smoke test: verdict: {obs.one_line_verdict}")

        client.close(session_id)
        logger.success("Smoke test passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slide Skill OpenEnv client")
    parser.add_argument(
        "--server", default=SERVER_URL, help="Server base URL"
    )
    parser.add_argument(
        "--max-steps", type=int, default=7, help="Max optimization steps"
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Run a single step smoke test instead of the full loop",
    )
    args = parser.parse_args()

    if args.smoke_test:
        smoke_test(server_url=args.server)
    else:
        run_optimization_loop(server_url=args.server, max_steps=args.max_steps)
