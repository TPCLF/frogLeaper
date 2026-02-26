from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse
from app.services.orchestrator_service import OrchestratorService

router = APIRouter()


def get_orchestrator() -> OrchestratorService:
    from app.main import orchestrator_service

    return orchestrator_service


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "orchestrator"}


@router.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> ChatResponse:
    return await orchestrator.chat(request)


@router.post("/v1/chat/completions/stream")
async def chat_completion_stream(
    request: ChatRequest,
    orchestrator: OrchestratorService = Depends(get_orchestrator),
) -> StreamingResponse:
    return StreamingResponse(orchestrator.chat_stream(request), media_type="text/event-stream")
