from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Tuple

from app.schemas import ToolCall


JSON_BLOCK_RE = re.compile(r"\{[\s\S]*\}")


def extract_json_payload(text: str) -> Dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = JSON_BLOCK_RE.search(text)
    if not match:
        return {"assistant_response": text, "tool_calls": []}

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"assistant_response": text, "tool_calls": []}


def normalize_claude_code_json(model_text: str) -> Tuple[str, List[ToolCall], Dict[str, Any]]:
    payload = extract_json_payload(model_text)
    response = str(payload.get("assistant_response", ""))
    tools = payload.get("tool_calls", [])

    parsed_calls: List[ToolCall] = []
    if isinstance(tools, list):
        for i, t in enumerate(tools):
            if not isinstance(t, dict):
                continue
            parsed_calls.append(
                ToolCall(
                    id=str(t.get("id", f"call_{i+1}")),
                    name=str(t.get("name", "")),
                    arguments=t.get("arguments", {}) if isinstance(t.get("arguments", {}), dict) else {},
                )
            )

    return response, parsed_calls, payload
