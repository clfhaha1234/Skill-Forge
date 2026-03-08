"""Reference client for the Slide Skill environment."""

import argparse
import asyncio
import base64
import sys
from pathlib import Path

import httpx


async def run_episode(
    server_url: str,
    reference_dir: Path,
    task_prompt: str,
    max_steps: int = 7,
    smoke_test: bool = False,
):
    """Run one optimization episode against the server."""
    # Load reference images
    ref_images = []
    for img_path in sorted(reference_dir.glob("*.jpg")):
        ref_images.append(base64.b64encode(img_path.read_bytes()).decode())
    if not ref_images:
        print(f"ERROR: No .jpg files found in {reference_dir}")
        sys.exit(1)
    print(f"Loaded {len(ref_images)} reference images from {reference_dir}")

    async with httpx.AsyncClient(timeout=300.0) as client:
        # Reset
        print("\n--- Reset ---")
        reset_resp = await client.post(
            f"{server_url}/reset",
            json={
                "reference_images": ref_images,
                "task_prompt": task_prompt,
                "max_steps": 1 if smoke_test else max_steps,
            },
        )
        reset_resp.raise_for_status()
        obs = reset_resp.json()["observation"]
        print(f"Baseline score: {obs['total']}/100")
        print(f"Verdict: {obs.get('one_line_verdict', '')}")

        if smoke_test:
            print("\n--- Smoke Test: 1 step ---")
            step_resp = await client.post(
                f"{server_url}/step",
                json={"action": {"hint": None}},
            )
            step_resp.raise_for_status()
            obs = step_resp.json()["observation"]
            print(f"Step 1 score: {obs['total']}/100")
            print(f"Verdict: {obs.get('one_line_verdict', '')}")
            print(f"Done: {obs.get('done_reason')}")
            return

        # Optimization loop
        step = 0
        while not obs.get("done", False):
            step += 1
            print(f"\n--- Step {step} ---")
            step_resp = await client.post(
                f"{server_url}/step",
                json={"action": {"hint": None}},
            )
            step_resp.raise_for_status()
            obs = step_resp.json()["observation"]
            print(f"Score: {obs['total']}/100")
            print(f"Verdict: {obs.get('one_line_verdict', '')}")
            if obs.get("weaknesses"):
                print(f"Top weakness: {obs['weaknesses'][0]}")

        print(f"\n=== Episode Complete ===")
        print(f"Final score: {obs['total']}/100")
        print(f"Reason: {obs.get('done_reason')}")
        print(f"Skill files: {list(obs.get('skill_files', {}).keys())}")


def main():
    parser = argparse.ArgumentParser(description="Slide Skill OpenEnv Client")
    parser.add_argument(
        "--server", default="http://localhost:8000", help="Server URL"
    )
    parser.add_argument(
        "--references",
        default="output/reference",
        help="Directory with reference .jpg images",
    )
    parser.add_argument(
        "--task",
        default=(
            "Generate a 1-slide timeline PowerPoint about Dutch Hydrogen "
            "Strategy (2020-2035) in McKinsey consulting style."
        ),
        help="Task prompt",
    )
    parser.add_argument("--max-steps", type=int, default=7)
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args()

    asyncio.run(
        run_episode(
            server_url=args.server,
            reference_dir=Path(args.references),
            task_prompt=args.task,
            max_steps=args.max_steps,
            smoke_test=args.smoke_test,
        )
    )


if __name__ == "__main__":
    main()
