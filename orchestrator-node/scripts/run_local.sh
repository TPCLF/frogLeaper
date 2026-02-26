#!/usr/bin/env bash
set -euo pipefail

uvicorn app.main:app --host "${ORCH_HOST:-0.0.0.0}" --port "${ORCH_PORT:-8000}"
