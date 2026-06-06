"""Вложения Allure для отчётности."""

from __future__ import annotations

import json
from typing import Any

import allure


def attach_json(name: str, data: Any) -> None:
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_text(name: str, text: str) -> None:
    allure.attach(text, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_request(method: str, url: str, payload: Any = None) -> None:
    attach_text("Метод HTTP", method.upper())
    attach_text("URL запроса", url)
    if payload is not None:
        attach_json("Тело запроса", payload)


def attach_response(status_code: int, body: Any) -> None:
    attach_text("Код ответа", str(status_code))
    attach_json("Тело ответа", body)
