from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    inf_host: str = Field(default="0.0.0.0", alias="INF_HOST")
    inf_port: int = Field(default=9000, alias="INF_PORT")
    llama_server_url: str = Field(default="http://127.0.0.1:8080", alias="LLAMA_SERVER_URL")

    llama_cpp_server_bin: str = Field(default="/opt/llama.cpp/build/bin/llama-server", alias="LLAMA_CPP_SERVER_BIN")
    llama_model_path: str = Field(default="/models/model.gguf", alias="LLAMA_MODEL_PATH")
    llama_ctx_size: int = Field(default=8192, alias="LLAMA_CTX_SIZE")
    llama_n_gpu_layers: int = Field(default=0, alias="LLAMA_N_GPU_LAYERS")
    llama_threads: int = Field(default=8, alias="LLAMA_THREADS")
    llama_batch: int = Field(default=512, alias="LLAMA_BATCH")
    auto_launch_llama: bool = Field(default=False, alias="AUTO_LAUNCH_LLAMA")


settings = Settings()
