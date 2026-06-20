"""Конфигурация проекта из переменных окружения."""

from __future__ import annotations

import os
from dataclasses import dataclass

import env_loader  # noqa: F401 — trello_ui/.env + trello_api/.env


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str
    api_token: str

    @classmethod
    def from_env(cls) -> Config:
        base_url = os.getenv("TRELLO_BASE_URL", "https://api.trello.com/1").rstrip("/")
        return cls(
            base_url=base_url,
            api_key=os.getenv("TRELLO_API_KEY", ""),
            api_token=os.getenv("TRELLO_API_TOKEN", ""),
        )

    def auth_params(self) -> dict[str, str]:
        return {"key": self.api_key, "token": self.api_token}

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("Не задан TRELLO_API_KEY")
        if not self.api_token:
            raise ValueError("Не задан TRELLO_API_TOKEN")
