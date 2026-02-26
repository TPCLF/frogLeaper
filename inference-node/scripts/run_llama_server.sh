#!/usr/bin/env bash
set -euo pipefail

: "${LLAMA_CPP_SERVER_BIN:=/opt/llama.cpp/build/bin/llama-server}"
: "${LLAMA_MODEL_PATH:=/models/qwen2.5-14b-instruct-q4_k_m.gguf}"
: "${LLAMA_CTX_SIZE:=12288}"
: "${LLAMA_N_GPU_LAYERS:=33}"
: "${LLAMA_THREADS:=12}"
: "${LLAMA_BATCH:=512}"
: "${LLAMA_PORT:=8080}"

exec "$LLAMA_CPP_SERVER_BIN" \
  -m "$LLAMA_MODEL_PATH" \
  --host 0.0.0.0 \
  --port "$LLAMA_PORT" \
  -c "$LLAMA_CTX_SIZE" \
  -ngl "$LLAMA_N_GPU_LAYERS" \
  -t "$LLAMA_THREADS" \
  -b "$LLAMA_BATCH"
