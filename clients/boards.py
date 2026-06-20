"""Операции с досками."""

from __future__ import annotations

import requests

from api.assertions import assert_status_code
from api.endpoints import Endpoints
from api.helpers import parse_json
from api.http import HttpClient
from api.validators import validate_board, validate_boards
from models.request.create_board import CreateBoardRequest
from models.response.board_response import BoardResponse


class BoardsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, payload: CreateBoardRequest) -> BoardResponse:
        response = self._http.request("POST", Endpoints.BOARDS, params=payload.to_api_params())
        assert_status_code(response, 200)
        return validate_board(parse_json(response))

    def get(self, board_id: str) -> BoardResponse:
        response = self._http.request("GET", Endpoints.BOARD_BY_ID.format(board_id=board_id))
        assert_status_code(response, 200)
        return validate_board(parse_json(response))

    def update(
        self,
        board_id: str,
        *,
        name: str | None = None,
        desc: str | None = None,
        closed: bool | None = None,
    ) -> BoardResponse:
        params: dict[str, str] = {}
        if name is not None:
            params["name"] = name
        if desc is not None:
            params["desc"] = desc
        if closed is not None:
            params["closed"] = str(closed).lower()
        response = self._http.request(
            "PUT",
            Endpoints.BOARD_BY_ID.format(board_id=board_id),
            params=params,
        )
        assert_status_code(response, 200)
        return validate_board(parse_json(response))

    def close(self, board_id: str) -> BoardResponse:
        return self.update(board_id, closed=True)

    def delete(self, board_id: str) -> requests.Response:
        response = self._http.request("DELETE", Endpoints.BOARD_BY_ID.format(board_id=board_id))
        assert_status_code(response, 200)
        return response

    def list_for_member(self) -> list[BoardResponse]:
        response = self._http.request("GET", Endpoints.MEMBERS_BOARDS)
        assert_status_code(response, 200)
        return validate_boards(parse_json(response))
