from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict

import yaml


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")


@lru_cache(maxsize=1)
def load_config(path: str | None = None) -> Dict[str, Any]:
    cfg_path = path or os.getenv("APP_CONFIG", DEFAULT_CONFIG_PATH)
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def get_mysql_dsn() -> str:
    cfg = load_config()
    db = cfg.get("mysql", {})
    user = db.get("user", "root")
    password = db.get("password", "root")
    host = db.get("host", "127.0.0.1")
    port = str(db.get("port", 3306))
    name = db.get("database", "prompt_db")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


def get_siliconflow_config() -> dict:
    cfg = load_config()
    sf = cfg.get("siliconflow", {})
    return {
        "api_key": sf.get("api_key", ""),
        "base_url": sf.get("base_url", "https://api.siliconflow.cn/v1"),
        "model": sf.get("model", "Qwen/Qwen2.5-72B-Instruct")
    }


