from __future__ import annotations

import asyncio
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class LlamaProcessManager:
    def __init__(self) -> None:
        self.process: Optional[asyncio.subprocess.Process] = None

    async def maybe_start(self) -> None:
        if not settings.auto_launch_llama:
            logger.info("AUTO_LAUNCH_LLAMA disabled; expecting external llama-server")
            return

        cmd = [
            settings.llama_cpp_server_bin,
            "-m",
            settings.llama_model_path,
            "--host",
            "0.0.0.0",
            "--port",
            "8080",
            "-c",
            str(settings.llama_ctx_size),
            "-ngl",
            str(settings.llama_n_gpu_layers),
            "-t",
            str(settings.llama_threads),
            "-b",
            str(settings.llama_batch),
        ]
        logger.info("Starting llama-server with command: %s", " ".join(cmd))
        self.process = await asyncio.create_subprocess_exec(*cmd)

    async def stop(self) -> None:
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()
            logger.info("llama-server terminated")
