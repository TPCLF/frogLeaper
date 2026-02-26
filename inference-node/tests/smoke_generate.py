#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

import httpx


def main() -> None:
    parser = argparse.ArgumentParser(description="Inference smoke test")
    parser.add_argument("--base-url", default="http://127.0.0.1:9000")
    parser.add_argument("--prompt", default="Return JSON with assistant_response and empty tool_calls.")
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    payload = {
        "prompt": args.prompt,
        "max_tokens": 128,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": args.stream,
    }

    if args.stream:
        with httpx.stream("POST", f"{args.base_url}/generate/stream", json=payload, timeout=None) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    print(line)
        return

    r = httpx.post(f"{args.base_url}/generate", json=payload, timeout=120)
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()
