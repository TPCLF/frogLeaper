from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    orch_host: str = Field(default="0.0.0.0", alias="ORCH_HOST")
    orch_port: int = Field(default=8000, alias="ORCH_PORT")
    orch_db_path: str = Field(default="/app/data/memory.db", alias="ORCH_DB_PATH")
    orch_config_file: str = Field(default="/app/config/orchestrator.example.yaml", alias="ORCH_CONFIG_FILE")

    inference_base_url: str = Field(default="http://127.0.0.1:9000", alias="INFERENCE_BASE_URL")
    request_timeout_s: int = Field(default=120, alias="REQUEST_TIMEOUT_S")

    max_context_messages: int = Field(default=24, alias="MAX_CONTEXT_MESSAGES")
    summary_trigger_messages: int = Field(default=40, alias="SUMMARY_TRIGGER_MESSAGES")
    embedding_dim: int = Field(default=384, alias="EMBEDDING_DIM")


settings = Settings()


def load_yaml_config(path: Optional[str] = None) -> dict:
    cfg_path = Path(path or settings.orch_config_file)
    if not cfg_path.exists():
        return {}
    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data
