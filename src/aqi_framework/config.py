"""Configuration loading and path resolution."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ProjectConfig:
    """Resolved project configuration."""

    root: Path
    raw: dict[str, Any]

    def path(self, dotted_key: str) -> Path:
        value: Any = self.raw
        for part in dotted_key.split("."):
            value = value[part]
        return (self.root / str(value)).resolve()

    def get(self, dotted_key: str, default: Any = None) -> Any:
        value: Any = self.raw
        try:
            for part in dotted_key.split("."):
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default


def load_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path).resolve()
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ValueError(f"Configuration must contain a mapping: {config_path}")
    root = config_path.parent.parent
    return ProjectConfig(root=root, raw=raw)
