from __future__ import annotations

import logging
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.config import settings
from app.llama_client import LlamaCppClient
from app.llama_process import LlamaProcessManager
from app.schemas import GenerateRequest, GenerateResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")

app = FastAPI(title="LLM Co-op Inference", version="0.1.0")
llama_client = LlamaCppClient()
proc_manager = LlamaProcessManager()


@app.on_event("startup")
async def startup() -> None:
    await proc_manager.maybe_start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await proc_manager.stop()


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "inference",
        "llama_server_url": settings.llama_server_url,
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:
    payload = req.model_dump()
    payload["stream"] = False
    data = await llama_client.generate(payload)
    return GenerateResponse(**data)


@app.post("/generate/stream")
async def generate_stream(req: GenerateRequest) -> StreamingResponse:
    payload = req.model_dump()
    payload["stream"] = True

    async def event_iter() -> AsyncGenerator[str, None]:
        async for line in llama_client.stream_generate(payload):
            yield line + "\n"

    return StreamingResponse(event_iter(), media_type="application/x-ndjson")
