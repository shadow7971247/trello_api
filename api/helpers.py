"""Вспомогательные функции для работы с API."""

from __future__ import annotations

from typing import Any

import requests

from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from models.response.member_response import MemberResponse, WorkspaceResponse


def normalize_query_params(params: dict[str, Any]) -> dict[str, str]:
    """Trello API ожидает строки; bool в requests уходит как False/True и ломает запрос."""
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


def validate_board(data: dict[str, Any]) -> BoardResponse:
    return BoardResponse.model_validate(data)


def validate_list(data: dict[str, Any]) -> ListResponse:
    return ListResponse.model_validate(data)


def validate_card(data: dict[str, Any]) -> CardResponse:
    return CardResponse.model_validate(data)


def validate_member(data: dict[str, Any]) -> MemberResponse:
    return MemberResponse.model_validate(data)


def validate_boards(data: list[dict[str, Any]]) -> list[BoardResponse]:
    return [BoardResponse.model_validate(item) for item in data]


def validate_workspaces(data: list[dict[str, Any]]) -> list[WorkspaceResponse]:
    return [WorkspaceResponse.model_validate(item) for item in data]
