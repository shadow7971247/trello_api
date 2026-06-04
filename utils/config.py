"""Конфигурация проекта из переменных окружения."""

from __future__ import annotations

import os
from dataclasses import dataclass

import env_loader  # noqa: F401 — trello_ui/.env + trello_api/.env


@dataclass(frozen=True)
class Config:
    """Централизованная конфигурация для Trello API."""

    base_url: str
    api_key: str
    api_token: str

    @classmethod
    def from_env(cls) -> Config:
        base_url = os.getenv("TRELLO_BASE_URL", "https://api.trello.com/1").rstrip("/")
        api_key = os.getenv("TRELLO_API_KEY", "")
        api_token = os.getenv("TRELLO_API_TOKEN", "")
        return cls(base_url=base_url, api_key=api_key, api_token=api_token)

    def auth_params(self) -> dict[str, str]:
        return {"key": self.api_key, "token": self.api_token}

    def validate(self) -> None:
        missing = [
            name
            for name, value in (
                ("TRELLO_API_KEY", self.api_key),
                ("TRELLO_API_TOKEN", self.api_token),
            )
            if not value
        ]
        if missing:
            raise ValueError(
                f"Не заданы обязательные переменные окружения: {', '.join(missing)}"
            )


config = Config.from_env()
