# Inference Node Project

This project is the **generation-only node** for a two-node LLM co-op system.

## Responsibilities
- Accept prompt generation requests from orchestrator
- Forward requests to `llama.cpp` server
- Return generated text (JSON endpoint)
- Return token stream (`ndjson` endpoint)
- Optionally launch `llama-server` process

No memory, tool logic, or orchestration lives here.

## API
- `GET /health`
- `POST /generate`
- `POST /generate/stream`

## Folder Structure
```text
inference-node/
  app/
    config.py
    llama_client.py
    llama_process.py
    main.py
    schemas.py
  config/inference.example.yaml
  scripts/run_llama_server.sh
  scripts/run_inference_api.sh
  tests/smoke_generate.py
```

## Run (recommended for GPU speed)
### 1) Start llama.cpp server
```bash
cd inference-node
export LLAMA_CPP_SERVER_BIN=/opt/llama.cpp/build/bin/llama-server
export LLAMA_MODEL_PATH=/models/qwen2.5-14b-instruct-q4_k_m.gguf
./scripts/run_llama_server.sh
```

### 2) Start inference API service
```bash
cd inference-node
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
./scripts/run_inference_api.sh
```

## Smoke Test
```bash
python tests/smoke_generate.py --base-url http://127.0.0.1:9000
python tests/smoke_generate.py --base-url http://127.0.0.1:9000 --stream
```

## llama.cpp Build Suggestion (Ubuntu 22.04 + NVIDIA)
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build -j
```

## Hardware Notes (Current Inference Node)
Target: Ryzen 7 2700X, 62GB RAM, RTX 3050 8GB
- Start with `n_gpu_layers=33` for 14B Q4 model and tune upward/downward by VRAM usage.
- Keep context around `12288` initially; increase only if stable.
- Keep CPU threads around physical cores for prompt processing.
