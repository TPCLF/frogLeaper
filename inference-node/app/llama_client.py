from __future__ import annotations

import json
from typing import AsyncGenerator, Dict

import httpx

from app.config import settings


class LlamaCppClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or settings.llama_server_url).rstrip("/")

    async def generate(self, payload: Dict) -> Dict:
        llama_payload = {
            "prompt": payload["prompt"],
            "n_predict": payload["max_tokens"],
            "temperature": payload["temperature"],
            "top_p": payload["top_p"],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=180) as client:
            resp = await client.post(f"{self.base_url}/completion", json=llama_payload)
            resp.raise_for_status()
            data = resp.json()

        content = data.get("content", "")
        usage = {
            "prompt_tokens": int(data.get("tokens_evaluated", 0)),
            "completion_tokens": int(data.get("tokens_predicted", 0)),
        }
        return {
            "text": content,
            "finish_reason": data.get("stop_type"),
            "usage": usage,
            "raw": data,
        }

    async def stream_generate(self, payload: Dict) -> AsyncGenerator[str, None]:
        llama_payload = {
            "prompt": payload["prompt"],
            "n_predict": payload["max_tokens"],
            "temperature": payload["temperature"],
            "top_p": payload["top_p"],
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}/completion", json=llama_payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    token = data.get("content", "")
                    stop = bool(data.get("stop", False))
                    yield json.dumps({"token": token, "done": stop})

                    if stop:
                        return
