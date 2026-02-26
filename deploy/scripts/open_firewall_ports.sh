#!/usr/bin/env bash
set -euo pipefail

# Run on each host as needed.
# Orchestrator host: open 8000/tcp
# Inference host: open 9000/tcp (and 8080/tcp if exposing llama-server directly)

if ! command -v ufw >/dev/null 2>&1; then
  echo "ufw not installed; skipping"
  exit 0
fi

sudo ufw allow 8000/tcp || true
sudo ufw allow 9000/tcp || true

# Optional direct llama-server exposure
# sudo ufw allow 8080/tcp

sudo ufw reload
sudo ufw status
