"""Pydantic-валидация ответов Trello API."""

from __future__ import annotations

from typing import Any

from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from models.response.member_response import MemberResponse, WorkspaceResponse


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
