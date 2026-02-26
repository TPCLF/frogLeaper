#!/usr/bin/env bash
set -euo pipefail

uvicorn app.main:app --host "${INF_HOST:-0.0.0.0}" --port "${INF_PORT:-9000}"
