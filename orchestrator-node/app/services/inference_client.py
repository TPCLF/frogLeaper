from __future__ import annotations

from typing import AsyncGenerator, Dict, Optional

import httpx

from app.core.config import settings


class InferenceClient:
    def __init__(self, base_url: Optional[str] = None, timeout_s: Optional[int] = None) -> None:
        self.base_url = (base_url or settings.inference_base_url).rstrip("/")
        self.timeout_s = timeout_s or settings.request_timeout_s

    async def generate(self, payload: Dict) -> Dict:
        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            resp = await client.post(f"{self.base_url}/generate", json=payload)
            resp.raise_for_status()
            return resp.json()

    async def stream_generate(self, payload: Dict) -> AsyncGenerator[str, None]:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}/generate/stream", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line:
                        yield line
