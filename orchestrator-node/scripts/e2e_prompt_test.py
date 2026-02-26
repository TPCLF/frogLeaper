#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="E2E test: orchestrator -> inference -> memory")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--conversation-id", default="demo-conv-001")
    parser.add_argument("--prompt", default="Write a Python function that reverses a linked list.")
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    payload = {
        "conversation_id": args.conversation_id,
        "user_input": args.prompt,
        "system_prompt": "You are a coding assistant. Return strict JSON response.",
        "tools": [
            {
                "name": "read_file",
                "description": "Read a local file",
                "input_schema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            }
        ],
        "stream": args.stream,
    }

    if args.stream:
        with httpx.stream("POST", f"{args.base_url}/v1/chat/completions/stream", json=payload, timeout=None) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    print(line)
        return

    r = httpx.post(f"{args.base_url}/v1/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()
