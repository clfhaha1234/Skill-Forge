"""Agentic optimizer using Claude Opus 4.6 with file tools."""

import os

import anthropic

from slide_skill_env.skill_manager import SkillManager

OPTIMIZER_SYSTEM = """You are a slide design skill optimizer. You improve design rule files
so that slides generated from them better match the reference style.

You have tools to read, write, list, and delete files in the skill folder.
The skill folder contains markdown files (like DESIGN_RULES.md, EXAMPLES.md)
that guide a slide generator.

Based on the evaluation feedback, decide what changes
to make. You can:
- Edit existing files to fix issues identified in the feedback
- Add new files (e.g., COLOR_RULES.md, LAYOUT_PATTERNS.md) if the skill
  needs more structure
- Delete files that are counterproductive
- Add helper scripts if needed

Focus on the weaknesses identified by the evaluator. Make targeted changes
that address specific issues rather than rewriting everything."""

OPTIMIZER_TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file in the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to read"}
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file in the skill folder. Creates or overwrites.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to write"},
                "content": {"type": "string", "description": "Full file content to write"},
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "delete_file",
        "description": "Delete a file from the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Name of the file to delete"}
            },
            "required": ["filename"],
        },
    },
    {
        "name": "list_files",
        "description": "List all files currently in the skill folder.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def optimize_skill(
    skill_manager: SkillManager,
    evaluation: dict,
    hint: str | None = None,
    api_key: str | None = None,
) -> None:
    """Run the optimizer agent to improve skill files in-place.

    The optimizer works from evaluation feedback only (scores, strengths,
    weaknesses). It does NOT see reference images — those are only used
    by the evaluator (Gemini) as ground truth.

    Args:
        skill_manager: SkillManager pointing to the working skill folder.
        evaluation: Previous evaluation results (scores, strengths, weaknesses).
        hint: Optional guidance from the client.
        api_key: Anthropic API key.
    """
    key = api_key or os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=key)

    current_files = skill_manager.read_all()
    files_str = ""
    for name, content in current_files.items():
        files_str += f"\n### {name}\n```\n{content}\n```\n"

    content_parts = []

    feedback_text = (
        f"\n## Previous Evaluation\n"
        f"Total score: {evaluation.get('total', 'N/A')}/100\n\n"
        f"**Strengths:**\n"
    )
    for s in evaluation.get("strengths", []):
        feedback_text += f"- {s}\n"
    feedback_text += f"\n**Weaknesses (FIX THESE):**\n"
    for w in evaluation.get("weaknesses", []):
        feedback_text += f"- {w}\n"
    feedback_text += f"\n**Verdict:** {evaluation.get('one_line_verdict', '')}\n"

    content_parts.append({"type": "text", "text": feedback_text})
    content_parts.append({
        "type": "text",
        "text": f"\n## Current Skill Files\n{files_str}",
    })

    if hint:
        content_parts.append({
            "type": "text",
            "text": f"\n## Additional Guidance\n{hint}",
        })

    content_parts.append({
        "type": "text",
        "text": (
            "\nUse your tools to improve the skill files. Focus on fixing "
            "the weaknesses. Start by listing current files, then make changes."
        ),
    })

    messages = [{"role": "user", "content": content_parts}]

    for _ in range(20):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=OPTIMIZER_SYSTEM,
            messages=messages,
            tools=OPTIMIZER_TOOLS,
        )

        if response.stop_reason == "end_turn":
            break

        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        tool_results = []
        for block in assistant_content:
            if block.type == "tool_use":
                result = _execute_tool(skill_manager, block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break


def _execute_tool(skill_manager: SkillManager, tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result as a string."""
    try:
        if tool_name == "read_file":
            return skill_manager.read_file(tool_input["filename"])
        elif tool_name == "write_file":
            skill_manager.write_file(tool_input["filename"], tool_input["content"])
            return f"Written: {tool_input['filename']}"
        elif tool_name == "delete_file":
            skill_manager.delete_file(tool_input["filename"])
            return f"Deleted: {tool_input['filename']}"
        elif tool_name == "list_files":
            files = skill_manager.list_files()
            return "\n".join(files) if files else "(empty)"
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error: {e}"
