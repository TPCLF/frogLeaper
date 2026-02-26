# Two-Node LLM Co-op System (llama.cpp backend)

This repository contains two separate projects:

1. `orchestrator-node/` (Dockerized)
2. `inference-node/` (llama.cpp generation service)

## Separation of Duties
- **Orchestrator node**: context management, memory, summarization, Claude-Code JSON tool-call contract, network client to inference.
- **Inference node**: token generation only; thin API over llama.cpp.

## Quick Start Order
1. Start `llama.cpp` and `inference-node` on inference machine.
2. Start `orchestrator-node` on orchestrator machine.
3. Send prompts to orchestrator (`/v1/chat/completions` or `/v1/chat/completions/stream`).
4. For production-style startup, use `deploy/` bundle with LAN quickstart and systemd units.

## Compatibility
Designed for Ubuntu 22.04 on both nodes with host-specific config examples included.

## Deploy Bundle
See [deploy/README.md](/home/user/leapFrog/deploy/README.md) and
[deploy/docs/LAN_QUICKSTART.md](/home/user/leapFrog/deploy/docs/LAN_QUICKSTART.md).
