"""Проверки для API-тестов."""

from __future__ import annotations

import requests


def assert_equals(actual: object, expected: object, name: str) -> None:
    assert actual == expected, (
        f"{name}: ожидалось {expected!r}, получено {actual!r}"
    )


def assert_status_code(response: requests.Response, expected: int) -> None:
    assert_equals(response.status_code, expected, "HTTP status")
