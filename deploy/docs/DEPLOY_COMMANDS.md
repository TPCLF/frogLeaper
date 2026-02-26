# Deploy Commands

Run from `/home/user/leapFrog`.

## Orchestrator Node
```bash
./deploy/scripts/bootstrap.sh orchestrator
```

## Inference Node (single service; inference API launches llama-server if enabled)
```bash
./deploy/scripts/bootstrap.sh inference
```

## Inference Node Split Mode (separate llama-server + inference API services)
```bash
./deploy/scripts/bootstrap.sh inference-split
```

## LAN Validation Commands (pre-deploy or post-deploy)
```bash
./deploy/scripts/check_lan_connectivity.sh <orchestrator_ip> <inference_ip>
```

## Logs
```bash
journalctl -u llm-orchestrator.service -f
journalctl -u llm-inference.service -f
journalctl -u llama-server.service -f
```
