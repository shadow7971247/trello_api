"""Сохранение и загрузка контекста тестовых сущностей для UI-слоя."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CONTEXT_FILE = ARTIFACTS_DIR / "test-context.json"


def ensure_artifacts_dir() -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR


def save_test_context(data: dict[str, Any]) -> Path:
    ensure_artifacts_dir()
    CONTEXT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return CONTEXT_FILE


def load_test_context() -> dict[str, Any]:
    if not CONTEXT_FILE.is_file():
        raise FileNotFoundError(
            f"Файл контекста не найден: {CONTEXT_FILE}. "
            "Сначала выполните: pytest -m ui_setup"
        )
    return json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))


def remove_test_context_file() -> None:
    if CONTEXT_FILE.is_file():
        CONTEXT_FILE.unlink()


def context_exists() -> bool:
    return CONTEXT_FILE.is_file()
