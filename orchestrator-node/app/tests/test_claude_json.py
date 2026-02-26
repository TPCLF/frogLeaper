from app.services.claude_json import normalize_claude_code_json


def test_parse_tool_call_json() -> None:
    text = '{"assistant_response":"ok","tool_calls":[{"id":"1","name":"read_file","arguments":{"path":"README.md"}}]}'
    response, tool_calls, payload = normalize_claude_code_json(text)
    assert response == "ok"
    assert len(tool_calls) == 1
    assert tool_calls[0].name == "read_file"
    assert payload["assistant_response"] == "ok"
