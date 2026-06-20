"""Низкоуровневые HTTP-запросы к Trello API."""

from __future__ import annotations

from typing import Any

import allure
import requests

from api.helpers import normalize_query_params, parse_json
from utils.attach import attach_request, attach_response
from utils.config import Config
from utils.logger import get_logger, log_request, log_response


class HttpClient:
    """Отправка запросов без проверки статус-кода."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._session = requests.Session()
        self._logger = get_logger("trello_http")

    @property
    def config(self) -> Config:
        return self._config

    def build_url(self, path: str) -> str:
        return f"{self._config.base_url}{path}"

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.build_url(path)
        merged_params = {**self._config.auth_params(), **(params or {})}
        query_params = normalize_query_params(merged_params)

        log_request(self._logger, method, url, query_params if not json_body else json_body)
        attach_request(method, url, query_params if not json_body else json_body)

        with allure.step(f"Запрос {method.upper()} {path}"):
            response = self._session.request(
                method=method,
                url=url,
                params=query_params if json_body is None else self._config.auth_params(),
                json=json_body,
                timeout=30,
            )

        body = parse_json(response)
        log_response(self._logger, response.status_code, url, body)
        attach_response(response.status_code, body)
        return response
