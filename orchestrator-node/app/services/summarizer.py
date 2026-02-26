from __future__ import annotations

from typing import List

from app.schemas import Message
from app.services.inference_client import InferenceClient


class Summarizer:
    def __init__(self, inference_client: InferenceClient, model: str | None = None) -> None:
        self.inference_client = inference_client
        self.model = model

    async def summarize_messages(self, messages: List[Message]) -> str:
        content = "\n".join(f"[{m.role}] {m.content}" for m in messages)
        prompt = (
            "Summarize the conversation in under 180 words. "
            "Focus on goals, decisions, constraints, and open tasks.\n\n"
            f"{content}"
        )

        try:
            result = await self.inference_client.generate(
                {
                    "prompt": prompt,
                    "model": self.model,
                    "max_tokens": 220,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "stream": False,
                }
            )
            return result.get("text", "").strip()
        except Exception:
            # Deterministic fallback: keep last key messages.
            tail = messages[-8:]
            return " ".join(f"[{m.role}] {m.content}" for m in tail)[:1200]
