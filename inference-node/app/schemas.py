from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: Optional[str] = None
    max_tokens: int = 512
    temperature: float = 0.2
    top_p: float = 0.9
    stream: bool = False


class GenerateResponse(BaseModel):
    text: str
    finish_reason: Optional[str] = None
    usage: Dict[str, int] = Field(default_factory=dict)
    raw: Dict[str, Any] = Field(default_factory=dict)
