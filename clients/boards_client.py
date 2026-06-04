"""Boards business client."""

from __future__ import annotations

import requests

from clients.base_client import BaseClient
from models.request.create_board import CreateBoardRequest
from models.response.board_response import BoardResponse


class BoardsClient(BaseClient):
    def create_board(
        self,
        name: str,
        *,
        desc: str | None = None,
        default_lists: bool = False,
        permission_level: str = "private",
    ) -> BoardResponse:
        payload = CreateBoardRequest(
            name=name,
            desc=desc,
            default_lists=default_lists,
            prefs_permission_level=permission_level,
        )
        return self.api.create_board(payload)

    def get_board(self, board_id: str) -> BoardResponse:
        return self.api.get_board(board_id)

    def update_board(
        self,
        board_id: str,
        *,
        name: str | None = None,
        desc: str | None = None,
    ) -> BoardResponse:
        return self.api.update_board(board_id, name=name, desc=desc)

    def delete_board(self, board_id: str) -> requests.Response:
        return self.api.delete_board(board_id)

