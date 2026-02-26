#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <orchestrator|inference>"
  exit 1
fi

ROLE="$1"
ROOT="/home/user/leapFrog"

case "$ROLE" in
  orchestrator)
    cd "$ROOT/orchestrator-node"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cp -f "$ROOT/deploy/env/orchestrator.lan.env" .env
    mkdir -p data
    echo "Prepared orchestrator node at $PWD"
    ;;
  inference)
    cd "$ROOT/inference-node"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cp -f "$ROOT/deploy/env/inference.lan.env" .env
    echo "Prepared inference node at $PWD"
    ;;
  *)
    echo "Invalid role: $ROLE"
    echo "Expected: orchestrator | inference"
    exit 1
    ;;
esac
