# LAN Quick Start (Before Deploy)

Use this flow to connect orchestrator and inference hosts before enabling systemd services.

## 1) Wire and verify network
On both machines:
```bash
ip -4 addr show
ip route
```
Confirm both are on the same subnet (example: `192.168.1.x/24`).

Optional hostname mapping on each host (`/etc/hosts`):
```text
192.168.1.20 orchestrator-node
192.168.1.50 inference-node
```

## 2) Set LAN IP targets in env files
Edit:
- `/home/user/leapFrog/deploy/env/orchestrator.lan.env`
- `/home/user/leapFrog/deploy/env/inference.lan.env`

Minimum required edits:
- `INFERENCE_BASE_URL=http://<inference_ip>:9000`
- `LLAMA_MODEL_PATH=<absolute model path on inference host>`
- `LLAMA_CPP_SERVER_BIN=<llama-server binary path>`

## 3) Prepare both nodes (no systemd yet)
On orchestrator host:
```bash
cd /home/user/leapFrog
./deploy/scripts/prepare_node.sh orchestrator
```

On inference host:
```bash
cd /home/user/leapFrog
./deploy/scripts/prepare_node.sh inference
```

## 4) Start both services manually for LAN validation
On inference host:
```bash
cd /home/user/leapFrog/inference-node
source .venv/bin/activate
./scripts/run_inference_api.sh
```

If `AUTO_LAUNCH_LLAMA=false`, start llama.cpp separately:
```bash
cd /home/user/leapFrog/inference-node
./scripts/run_llama_server.sh
```

On orchestrator host:
```bash
cd /home/user/leapFrog/orchestrator-node
source .venv/bin/activate
./scripts/run_local.sh
```

## 5) Validate cross-node connectivity
From either host:
```bash
cd /home/user/leapFrog
./deploy/scripts/check_lan_connectivity.sh <orchestrator_ip> <inference_ip>
```

Run an end-to-end prompt from orchestrator:
```bash
cd /home/user/leapFrog/orchestrator-node
python scripts/e2e_prompt_test.py --base-url http://<orchestrator_ip>:8000
```

Verify memory persistence:
```bash
python scripts/verify_memory_update.py --base-url http://<orchestrator_ip>:8000 --db-path ./data/memory.db
```

## 6) Deploy with one command per node type
After LAN validation passes:

On orchestrator host:
```bash
cd /home/user/leapFrog
./deploy/scripts/bootstrap.sh orchestrator
```

On inference host (single-service mode):
```bash
cd /home/user/leapFrog
./deploy/scripts/bootstrap.sh inference
```

On inference host (split mode: dedicated llama-server service):
```bash
cd /home/user/leapFrog
./deploy/scripts/bootstrap.sh inference-split
```

For full command reference, see `/home/user/leapFrog/deploy/docs/DEPLOY_COMMANDS.md`.
