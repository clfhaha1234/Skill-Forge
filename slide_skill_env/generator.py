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

    # Extract file_ids from response
    file_ids = _extract_file_ids(response)
    if not file_ids:
        raise RuntimeError(
            "No file was generated. Response: "
            + str([b.type for b in response.content])
        )

    # Download files — find the .pptx (PK zip header)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for file_id in file_ids:
        file_resp = client.beta.files.download(
            file_id=file_id, betas=["files-api-2025-04-14"]
        )
        data = file_resp.read()
        # PK\x03\x04 is the ZIP/PPTX magic header
        if data[:4] == b"PK\x03\x04":
            output_path.write_bytes(data)
            return output_path

    raise RuntimeError(
        f"Generated {len(file_ids)} files but none were .pptx (ZIP) format"
    )


def _extract_file_ids(response) -> list[str]:
    """Extract all file_ids from code execution response blocks."""
    file_ids = []
    for block in response.content:
        if block.type == "bash_code_execution_tool_result":
            result = block.content
            if hasattr(result, "content") and isinstance(result.content, list):
                for item in result.content:
                    if hasattr(item, "file_id"):
                        file_ids.append(item.file_id)
    return file_ids
