#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <orchestrator|inference|inference-split>"
  exit 1
fi

ROLE="$1"
ROOT="/home/user/leapFrog/deploy/systemd"

install_unit() {
  local unit_file="$1"
  sudo cp "$ROOT/$unit_file" /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable --now "${unit_file}"
}

case "$ROLE" in
  orchestrator)
    install_unit "llm-orchestrator.service"
    sudo systemctl status llm-orchestrator.service --no-pager -n 30
    ;;
  inference)
    install_unit "llm-inference.service"
    sudo systemctl status llm-inference.service --no-pager -n 30
    ;;
  inference-split)
    echo "Ensure AUTO_LAUNCH_LLAMA=false in /home/user/leapFrog/inference-node/.env for split mode."
    install_unit "llama-server.service"
    install_unit "llm-inference.service"
    sudo systemctl status llama-server.service --no-pager -n 30
    sudo systemctl status llm-inference.service --no-pager -n 30
    ;;
  *)
    echo "Invalid role: $ROLE"
    echo "Expected: orchestrator | inference | inference-split"
    exit 1
    ;;
esac
