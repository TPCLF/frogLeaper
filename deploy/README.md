# Deploy Bundle

This folder provides one deployment bundle for both node roles.

## Contents
- `env/orchestrator.lan.env`: preconfigured orchestrator env for LAN
- `env/inference.lan.env`: preconfigured inference env for LAN
- `systemd/llm-orchestrator.service`: orchestrator API service
- `systemd/llm-inference.service`: inference API service
- `systemd/llama-server.service`: optional standalone llama.cpp service
- `scripts/prepare_node.sh`: installs venv deps and copies role env
- `scripts/install_systemd.sh`: installs and enables role service units
- `scripts/bootstrap.sh`: one-command role deployment (prepare + install)
- `scripts/check_lan_connectivity.sh`: ping + health endpoint checks
- `scripts/open_firewall_ports.sh`: optional UFW rules helper
- `docs/LAN_QUICKSTART.md`: LAN setup before deploy
- `docs/DEPLOY_COMMANDS.md`: command list for each deployment mode

## Recommended sequence
1. Complete LAN setup and manual run tests in `docs/LAN_QUICKSTART.md`.
2. Deploy each host with one command using `scripts/bootstrap.sh`.
3. Check logs:
```bash
journalctl -u llm-orchestrator.service -f
journalctl -u llm-inference.service -f
```
