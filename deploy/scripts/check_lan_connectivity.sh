#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <orchestrator_ip> <inference_ip>"
  exit 1
fi

ORCH_IP="$1"
INF_IP="$2"

echo "[1/4] Ping inference from orchestrator host context"
ping -c 2 "$INF_IP"

echo "[2/4] Ping orchestrator from inference host context"
ping -c 2 "$ORCH_IP"

echo "[3/4] Check inference health endpoint"
curl -fsS "http://$INF_IP:9000/health" | sed 's/.*/inference health: &/'

echo "[4/4] Check orchestrator health endpoint"
curl -fsS "http://$ORCH_IP:8000/health" | sed 's/.*/orchestrator health: &/'

echo "LAN connectivity checks passed"
