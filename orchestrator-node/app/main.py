from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.services.inference_client import InferenceClient
from app.services.memory_service import MemoryService
from app.services.orchestrator_service import OrchestratorService

configure_logging()

app = FastAPI(title="LLM Co-op Orchestrator", version="0.1.0")

memory_service = MemoryService(db_path=settings.orch_db_path, embedding_dim=settings.embedding_dim)
inference_client = InferenceClient()
orchestrator_service = OrchestratorService(memory_service=memory_service, inference_client=inference_client)


@app.on_event("startup")
async def startup() -> None:
    await memory_service.init()


app.include_router(router)
