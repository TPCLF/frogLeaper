#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sqlite3

import httpx


def get_count(db_path: str, conversation_id: str) -> int:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "SELECT COUNT(*) FROM messages WHERE conversation_id = ?",
            (conversation_id,),
        )
        row = cur.fetchone()
        return int(row[0])
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify memory updates after orchestrator call")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--conversation-id", default="verify-memory-001")
    parser.add_argument("--db-path", default=os.getenv("ORCH_DB_PATH", "./data/memory.db"))
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    before = get_count(args.db_path, args.conversation_id)

    payload = {
        "conversation_id": args.conversation_id,
        "user_input": "Return JSON with assistant_response and empty tool_calls.",
        "stream": args.stream,
        "tools": [],
    }

    if args.stream:
        with httpx.stream("POST", f"{args.base_url}/v1/chat/completions/stream", json=payload, timeout=None) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    print(line)
    else:
        r = httpx.post(f"{args.base_url}/v1/chat/completions", json=payload, timeout=120)
        r.raise_for_status()
        print(json.dumps(r.json(), indent=2))

    after = get_count(args.db_path, args.conversation_id)
    print(json.dumps({"before": before, "after": after, "delta": after - before}, indent=2))


if __name__ == "__main__":
    main()
