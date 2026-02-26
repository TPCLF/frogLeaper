from __future__ import annotations

import json
import logging
from typing import AsyncGenerator, Dict, List, Optional

from app.core.config import load_yaml_config, settings
from app.schemas import ChatRequest, ChatResponse, Message
from app.services.claude_json import normalize_claude_code_json
from app.services.inference_client import InferenceClient
from app.services.memory_service import MemoryService
from app.services.prompt_builder import build_prompt
from app.services.summarizer import Summarizer

logger = logging.getLogger(__name__)


class OrchestratorService:
    def __init__(self, memory_service: MemoryService, inference_client: InferenceClient) -> None:
        self.memory = memory_service
        self.inference = inference_client
        cfg = load_yaml_config()
        inf_cfg = cfg.get("inference", {})
        self.default_model = inf_cfg.get("model")
        self.default_temperature = float(inf_cfg.get("temperature", 0.2))
        self.default_top_p = float(inf_cfg.get("top_p", 0.9))
        self.default_max_tokens = int(inf_cfg.get("max_tokens", 768))
        self.summarizer = Summarizer(inference_client=inference_client, model=self.default_model)

    async def _build_payload(self, request: ChatRequest) -> Dict:
        recent = await self.memory.get_recent_messages(request.conversation_id, settings.max_context_messages)
        semantic = await self.memory.get_semantic_memories(request.conversation_id, request.user_input, top_k=5)
        summary = await self.memory.get_summary(request.conversation_id)

        prompt = build_prompt(
            user_input=request.user_input,
            recent_messages=recent,
            semantic_memories=semantic,
            tools=request.tools,
            system_prompt=request.system_prompt,
            conversation_summary=summary,
        )

        return {
            "prompt": prompt,
            "model": self.default_model,
            "max_tokens": request.max_tokens or self.default_max_tokens,
            "temperature": request.temperature if request.temperature is not None else self.default_temperature,
            "top_p": request.top_p if request.top_p is not None else self.default_top_p,
            "stream": request.stream,
        }

    async def _persist_and_maybe_summarize(self, request: ChatRequest, assistant_text: str) -> None:
        await self.memory.add_message(
            request.conversation_id,
            Message(role="user", content=request.user_input),
        )
        await self.memory.add_message(
            request.conversation_id,
            Message(role="assistant", content=assistant_text),
        )

        count = await self.memory.get_message_count(request.conversation_id)
        if count >= settings.summary_trigger_messages:
            msgs = await self.memory.get_recent_messages(request.conversation_id, 40)
            summary = await self.summarizer.summarize_messages(msgs)
            await self.memory.upsert_summary(request.conversation_id, summary)

    async def chat(self, request: ChatRequest) -> ChatResponse:
        payload = await self._build_payload(request)
        payload["stream"] = False
        model_result = await self.inference.generate(payload)
        model_text = model_result.get("text", "")
        output_text, tool_calls, raw_payload = normalize_claude_code_json(model_text)

        memory_text = output_text.strip() or model_text
        await self._persist_and_maybe_summarize(request, memory_text)

        return ChatResponse(
            conversation_id=request.conversation_id,
            output_text=output_text,
            tool_calls=tool_calls,
            raw_model_payload={"inference": model_result, "parsed": raw_payload},
        )

    async def chat_stream(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        payload = await self._build_payload(request)
        payload["stream"] = True

        buffer: List[str] = []
        async for line in self.inference.stream_generate(payload):
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            token = data.get("token", "")
            if token:
                buffer.append(token)
                yield f"data: {json.dumps({'token': token})}\n\n"

            if data.get("done"):
                full_text = "".join(buffer)
                output_text, tool_calls, _ = normalize_claude_code_json(full_text)
                memory_text = output_text.strip() or full_text
                await self._persist_and_maybe_summarize(request, memory_text)
                yield (
                    "data: "
                    + json.dumps(
                        {
                            "done": True,
                            "assistant_response": output_text,
                            "tool_calls": [t.model_dump() for t in tool_calls],
                        }
                    )
                    + "\n\n"
                )
                return

        full_text = "".join(buffer)
        if full_text:
            await self._persist_and_maybe_summarize(request, full_text)
            yield f"data: {json.dumps({'done': True})}\n\n"
