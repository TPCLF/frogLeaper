from app.schemas import Message, ToolDef
from app.services.memory_service import MemoryItem
from app.services.prompt_builder import build_prompt


def test_build_prompt_includes_tools_and_input() -> None:
    prompt = build_prompt(
        user_input="hello",
        recent_messages=[Message(role="user", content="hi")],
        semantic_memories=[MemoryItem(role="assistant", content="foo", score=0.5)],
        tools=[ToolDef(name="x", description="d", input_schema={"type": "object"})],
        system_prompt=None,
        conversation_summary=None,
    )
    assert "AVAILABLE TOOLS" in prompt
    assert "CURRENT USER INPUT" in prompt
