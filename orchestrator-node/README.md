# Orchestrator Node Project

This project is the **context/orchestration node** for a two-node LLM co-op system.

## Responsibilities
- Manage conversation memory (SQLite + embeddings)
- Assemble prompts with recent history + semantic recall + summary
- Enforce Claude-Code compatible JSON response contract
- Parse tool calls from model JSON output
- Call inference node for generation (sync or streaming)
- Persist user/assistant turns and rolling summaries

## API
- `GET /health`
- `POST /v1/chat/completions`
- `POST /v1/chat/completions/stream` (SSE)

## Claude-Code JSON Contract
Model should return JSON:
```json
{
  "assistant_response": "text for Claude-Code",
  "tool_calls": [
    {
      "id": "call_1",
      "name": "read_file",
      "arguments": {"path": "src/main.py"}
    }
  ]
}
```
If no tools are needed, return `"tool_calls": []`.

## Folder Structure
```text
orchestrator-node/
  app/
    api/routes.py
    core/config.py
    services/
      claude_json.py
      embedding_service.py
      inference_client.py
      memory_service.py
      orchestrator_service.py
      prompt_builder.py
      summarizer.py
    schemas/chat.py
    tests/
  config/orchestrator.example.yaml
  data/
  scripts/e2e_prompt_test.py
  scripts/verify_memory_update.py
  scripts/run_local.sh
  Dockerfile
  docker-compose.yml
```

## Run (Docker)
1. Copy `.env.example` to `.env` and set `INFERENCE_BASE_URL`.
2. Start:
```bash
docker compose up --build
```

## Run (Local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./scripts/run_local.sh
```

## Test Script (orchestrator -> inference)
Non-streaming:
```bash
python scripts/e2e_prompt_test.py --base-url http://127.0.0.1:8000
```
Streaming:
```bash
python scripts/e2e_prompt_test.py --base-url http://127.0.0.1:8000 --stream
```
Verify memory update after request:
```bash
python scripts/verify_memory_update.py --base-url http://127.0.0.1:8000 --db-path ./data/memory.db
python scripts/verify_memory_update.py --base-url http://127.0.0.1:8000 --db-path ./data/memory.db --stream
```

## Hardware Notes (Current Orchestrator)
Target: i7-3770S, 16GB RAM, GTX 960 4GB
- Keep orchestrator lightweight and CPU-focused.
- Offload all generation to inference node.
- Use small embedding dimension (`384`) to limit memory overhead.
