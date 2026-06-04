"""Base business client for Trello API.

This layer provides stable, reusable business methods for UI and Mobile tests.
It is intentionally thin: HTTP + Allure/logging live in `api.client.TrelloApiClient`.
"""

from __future__ import annotations

from api.client import TrelloApiClient
from utils.config import Config, config as default_config


class BaseClient:
    def __init__(
        self,
        api: TrelloApiClient | None = None,
        *,
        config: Config | None = None,
    ) -> None:
        cfg = config or default_config
        cfg.validate()
        self._api = api or TrelloApiClient(cfg)

    @property
    def api(self) -> TrelloApiClient:
        return self._api

