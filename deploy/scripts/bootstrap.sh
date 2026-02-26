#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <orchestrator|inference|inference-split>"
  exit 1
fi

ROLE="$1"
ROOT="/home/user/leapFrog/deploy/scripts"

case "$ROLE" in
  orchestrator)
    "$ROOT/prepare_node.sh" orchestrator
    "$ROOT/install_systemd.sh" orchestrator
    ;;
  inference)
    "$ROOT/prepare_node.sh" inference
    "$ROOT/install_systemd.sh" inference
    ;;
  inference-split)
    "$ROOT/prepare_node.sh" inference
    "$ROOT/install_systemd.sh" inference-split
    ;;
  *)
    echo "Invalid role: $ROLE"
    echo "Expected: orchestrator | inference | inference-split"
    exit 1
    ;;
esac

echo "Bootstrap complete for role: $ROLE"
