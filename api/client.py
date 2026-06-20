"""Фасад Trello API — совместимый интерфейс для тестов."""

from __future__ import annotations

from typing import Any

import requests

from api.http import HttpClient
from clients.boards import BoardsClient
from clients.cards import CardsClient
from clients.checklists import ChecklistsClient
from clients.lists import ListsClient
from clients.members import MembersClient
from models.request.create_board import CreateBoardRequest
from models.request.create_card import CreateCardRequest
from models.request.create_list import CreateListRequest
from models.request.update_card import UpdateCardRequest
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from models.response.member_response import MemberResponse, WorkspaceResponse
from utils.config import Config


class TrelloApiClient:
    """Единая точка входа: делегирует вызовы клиентам по сущностям."""

    def __init__(self, config: Config) -> None:
        http = HttpClient(config)
        self._http = http
        self.boards = BoardsClient(http)
        self.lists = ListsClient(http)
        self.cards = CardsClient(http)
        self.members = MembersClient(http)
        self.checklists = ChecklistsClient(http)

    @property
    def config(self) -> Config:
        return self._http.config

    def get_current_user(self) -> MemberResponse:
        return self.members.get_current()

    def create_board(self, payload: CreateBoardRequest) -> BoardResponse:
        return self.boards.create(payload)

    def get_board(self, board_id: str) -> BoardResponse:
        return self.boards.get(board_id)

    def update_board(
        self,
        board_id: str,
        *,
        name: str | None = None,
        desc: str | None = None,
        closed: bool | None = None,
    ) -> BoardResponse:
        return self.boards.update(board_id, name=name, desc=desc, closed=closed)

    def close_board(self, board_id: str) -> BoardResponse:
        return self.boards.close(board_id)

    def delete_board(self, board_id: str) -> requests.Response:
        return self.boards.delete(board_id)

    def create_list(self, payload: CreateListRequest) -> ListResponse:
        return self.lists.create(payload)

    def get_list(self, list_id: str) -> ListResponse:
        return self.lists.get(list_id)

    def update_list(self, list_id: str, *, name: str) -> ListResponse:
        return self.lists.update(list_id, name=name)

    def create_card(self, payload: CreateCardRequest) -> CardResponse:
        return self.cards.create(payload)

    def get_card(self, card_id: str) -> CardResponse:
        return self.cards.get(card_id)

    def update_card(self, card_id: str, payload: UpdateCardRequest) -> CardResponse:
        return self.cards.update(card_id, payload)

    def delete_card(self, card_id: str) -> requests.Response:
        return self.cards.delete(card_id)

    def move_card(self, card_id: str, target_list_id: str) -> CardResponse:
        return self.cards.move(card_id, target_list_id)

    def archive_card(self, card_id: str) -> CardResponse:
        return self.cards.archive(card_id)

    def create_checklist(self, card_id: str, name: str) -> dict[str, Any]:
        return self.checklists.create(card_id, name)

    def add_checkitem(self, checklist_id: str, name: str, checked: bool = False) -> dict[str, Any]:
        return self.checklists.add_item(checklist_id, name, checked)

    def get_member_boards(self) -> list[BoardResponse]:
        return self.boards.list_for_member()

    def get_workspaces(self) -> list[WorkspaceResponse]:
        return self.members.get_workspaces()

    def raw_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Запрос без проверки статуса — для негативных сценариев."""
        return self._http.request(method, path, params=params)
