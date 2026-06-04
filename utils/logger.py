"""Структурированное логирование HTTP-запросов и ответов."""

from __future__ import annotations

import json
import logging
from typing import Any

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "trello_api_tests") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def _serialize_payload(payload: Any) -> str:
    if payload is None:
        return "null"
    if isinstance(payload, (dict, list)):
        return json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    return str(payload)


def log_request(
    logger: logging.Logger,
    method: str,
    endpoint: str,
    payload: Any = None,
) -> None:
    logger.info(
        "REQUEST | %s %s | payload=%s",
        method.upper(),
        endpoint,
        _serialize_payload(payload),
    )


def log_response(
    logger: logging.Logger,
    status_code: int,
    endpoint: str,
    body: Any = None,
) -> None:
    logger.info(
        "RESPONSE | %s %s | status=%s | body=%s",
        "->",
        endpoint,
        status_code,
        _serialize_payload(body),
    )
