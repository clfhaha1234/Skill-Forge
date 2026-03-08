"""Generate slides using Claude Sonnet 4.6 + managed pptx skill."""

import os
from pathlib import Path

import anthropic


def generate_slide(
    task_prompt: str,
    skill_files: dict[str, str],
    output_path: Path,
    api_key: str | None = None,
) -> Path:
    """Generate a .pptx slide using Claude Sonnet with the pptx skill.

    Args:
        task_prompt: What slide to generate.
        skill_files: Skill folder contents {filename: content}.
        output_path: Where to save the downloaded .pptx file.
        api_key: Anthropic API key (falls back to ANTHROPIC_API_KEY env var).

    Returns:
        Path to the saved .pptx file.

    Raises:
        RuntimeError: If generation or download fails.
    """
    key = api_key or os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)

    # Build message with skill files as context
    skill_context = ""
    for filename, content in skill_files.items():
        skill_context += f"\n### {filename}\n```\n{content}\n```\n"

    message_content = (
        f"Follow these design rules exactly when generating the slide:\n"
        f"{skill_context}\n\n"
        f"## Task\n{task_prompt}"
    )

    response = client.beta.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16384,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
            ]
        },
        messages=[{"role": "user", "content": message_content}],
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )

    # Extract file_id from response
    file_id = _extract_file_id(response)
    if not file_id:
        raise RuntimeError(
            "No file was generated. Response: "
            + str([b.type for b in response.content])
        )

    # Download the file
    file_content = client.beta.files.download(
        file_id=file_id, betas=["files-api-2025-04-14"]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        file_content.write_to_file(f.name)

    return output_path


def _extract_file_id(response) -> str | None:
    """Extract file_id from a code execution response."""
    for block in response.content:
        if block.type == "tool_result":
            for item in block.content:
                if hasattr(item, "file_id"):
                    return item.file_id
        if block.type == "server_tool_result":
            for item in getattr(block, "content", []):
                if hasattr(item, "file_id"):
                    return item.file_id
    return None
