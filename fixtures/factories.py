"""Создание сущностей Trello через API."""

from __future__ import annotations

from api.client import TrelloApiClient
from fixtures.generators import board_name, card_description, card_name, checklist_name, list_name
from models.request.create_board import CreateBoardRequest
from models.request.create_card import CreateCardRequest
from models.request.create_list import CreateListRequest
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse


def prepare_board(
    client: TrelloApiClient,
    name: str | None = None,
    *,
    permission_level: str = "private",
    desc: str | None = None,
) -> BoardResponse:
    payload = CreateBoardRequest(
        name=name or board_name(),
        desc=desc,
        prefs_permission_level=permission_level,
    )
    return client.create_board(payload)


def prepare_public_board(
    client: TrelloApiClient,
    name: str | None = None,
    *,
    desc: str | None = None,
) -> BoardResponse:
    return prepare_board(client, name=name, permission_level="public", desc=desc)


def prepare_list(
    client: TrelloApiClient,
    board_id: str,
    name: str | None = None,
) -> ListResponse:
    payload = CreateListRequest(name=name or list_name(), id_board=board_id)
    return client.create_list(payload)


def prepare_card(
    client: TrelloApiClient,
    list_id: str,
    name: str | None = None,
    desc: str | None = None,
) -> CardResponse:
    payload = CreateCardRequest(
        name=name or card_name(),
        id_list=list_id,
        desc=desc or card_description(),
    )
    return client.create_card(payload)


def prepare_checklist(
    client: TrelloApiClient,
    card_id: str,
    name: str | None = None,
) -> dict:
    return client.create_checklist(card_id, name or checklist_name())
