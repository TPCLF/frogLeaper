from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


Role = Literal["system", "user", "assistant", "tool"]


class Message(BaseModel):
    role: Role
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None


class ToolDef(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., min_length=1)
    user_input: str = Field(..., min_length=1)
    system_prompt: Optional[str] = None
    tools: List[ToolDef] = Field(default_factory=list)
    stream: bool = True
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: str
    output_text: str
    tool_calls: List[ToolCall] = Field(default_factory=list)
    raw_model_payload: Dict[str, Any]


class InferenceGenerateRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: int
    temperature: float
    top_p: float
    stream: bool = True


class InferenceGenerateResponse(BaseModel):
    text: str
    finish_reason: Optional[str] = None
    usage: Dict[str, int] = Field(default_factory=dict)
    raw: Dict[str, Any] = Field(default_factory=dict)
