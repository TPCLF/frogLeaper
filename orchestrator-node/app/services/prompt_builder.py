from __future__ import annotations

import json
from typing import List, Optional

from app.schemas import Message, ToolDef
from app.services.memory_service import MemoryItem


def _render_messages(messages: List[Message]) -> str:
    return "\n".join([f"[{m.role}] {m.content}" for m in messages])


def build_prompt(
    user_input: str,
    recent_messages: List[Message],
    semantic_memories: List[MemoryItem],
    tools: List[ToolDef],
    system_prompt: Optional[str],
    conversation_summary: Optional[str],
) -> str:
    tools_json = json.dumps([t.model_dump() for t in tools], indent=2)

    memory_lines = "\n".join([
        f"- ({mem.score:.3f}) [{mem.role}] {mem.content}" for mem in semantic_memories
    ]) or "- none"

    sys_prompt = system_prompt or (
        "You are a cooperative coding assistant for Claude-Code. "
        "Return a JSON object only."
    )

    summary_block = conversation_summary or "No summary yet."

    return f"""
{sys_prompt}

JSON RESPONSE CONTRACT:
{{
  "assistant_response": "string",
  "tool_calls": [
    {{"id": "call_1", "name": "tool_name", "arguments": {{"key": "value"}}}}
  ]
}}

If no tool is needed, return an empty list for tool_calls.

AVAILABLE TOOLS:
{tools_json}

CONVERSATION SUMMARY:
{summary_block}

SEMANTIC MEMORY CANDIDATES:
{memory_lines}

RECENT MESSAGES:
{_render_messages(recent_messages)}

CURRENT USER INPUT:
[user] {user_input}
""".strip()
