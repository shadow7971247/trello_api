"""Парсинг и нормализация HTTP-данных."""

from __future__ import annotations

from typing import Any

import requests


def normalize_query_params(params: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in params.items():
        if isinstance(value, bool):
            normalized[key] = str(value).lower()
        elif value is not None:
            normalized[key] = str(value)
    return normalized


def parse_json(response: requests.Response) -> Any:
    text = (response.text or "").strip()
    if not text:
        return None
    try:
        return response.json()
    except ValueError:
        return {"_raw": text}
