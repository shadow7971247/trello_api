"""HTTP-клиент Trello API — единая точка входа для всех запросов."""

from __future__ import annotations

from typing import Any

import allure
import requests

from api.endpoints import Endpoints
from api.helpers import (
    normalize_query_params,
    parse_json,
    validate_board,
    validate_boards,
    validate_card,
    validate_list,
    validate_member,
    validate_workspaces,
)
from models.request.create_board import CreateBoardRequest
from models.request.create_card import CreateCardRequest
from models.request.create_list import CreateListRequest
from models.request.update_card import UpdateCardRequest
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from models.response.member_response import MemberResponse, WorkspaceResponse
from utils.attach import attach_request, attach_response
from utils.config import Config
from utils.logger import get_logger, log_request, log_response


class TrelloApiClient:
    """Переиспользуемый клиент Trello REST API."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._session = requests.Session()
        self._logger = get_logger("trello_api_client")

    @property
    def config(self) -> Config:
        return self._config

    def _build_url(self, path: str) -> str:
        return f"{self._config.base_url}{path}"

    def _auth_params(self) -> dict[str, str]:
        return self._config.auth_params()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        validate: bool = True,
    ) -> requests.Response:
        url = self._build_url(path)
        merged_params = {**self._auth_params(), **(params or {})}
        query_params = normalize_query_params(merged_params)

        log_request(self._logger, method, url, query_params if not json_body else json_body)
        attach_request(method, url, query_params if not json_body else json_body)

        with allure.step(f"{method.upper()} {path}"):
            response = self._session.request(
                method=method,
                url=url,
                params=query_params if json_body is None else self._auth_params(),
                json=json_body,
                timeout=30,
            )

        body = parse_json(response)
        log_response(self._logger, response.status_code, url, body)
        attach_response(response.status_code, body)

        if validate and response.status_code >= 400:
            raise requests.HTTPError(
                f"HTTP {response.status_code} для {method.upper()} {path}: {response.text}",
                response=response,
            )

        return response

    def get_current_user(self) -> MemberResponse:
        response = self._request("GET", Endpoints.MEMBERS_ME)
        return validate_member(parse_json(response))

    def create_board(self, payload: CreateBoardRequest) -> BoardResponse:
        response = self._request("POST", Endpoints.BOARDS, params=payload.to_api_params())
        return validate_board(parse_json(response))

    def get_board(self, board_id: str) -> BoardResponse:
        response = self._request("GET", Endpoints.BOARD_BY_ID.format(board_id=board_id))
        return validate_board(parse_json(response))

    def update_board(
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
        response = self._request(
            "PUT",
            Endpoints.BOARD_BY_ID.format(board_id=board_id),
            params=params,
        )
        return validate_board(parse_json(response))

    def close_board(self, board_id: str) -> BoardResponse:
        """Закрыть (архивировать) доску."""
        return self.update_board(board_id, closed=True)

    def delete_board(self, board_id: str) -> requests.Response:
        return self._request("DELETE", Endpoints.BOARD_BY_ID.format(board_id=board_id))

    def create_list(self, payload: CreateListRequest) -> ListResponse:
        response = self._request("POST", Endpoints.LISTS, params=payload.to_api_params())
        return validate_list(parse_json(response))

    def get_list(self, list_id: str) -> ListResponse:
        response = self._request("GET", Endpoints.LIST_BY_ID.format(list_id=list_id))
        return validate_list(parse_json(response))

    def update_list(self, list_id: str, *, name: str) -> ListResponse:
        response = self._request(
            "PUT",
            Endpoints.LIST_BY_ID.format(list_id=list_id),
            params={"name": name},
        )
        return validate_list(parse_json(response))

    def create_card(self, payload: CreateCardRequest) -> CardResponse:
        response = self._request("POST", Endpoints.CARDS, params=payload.to_api_params())
        return validate_card(parse_json(response))

    def get_card(self, card_id: str) -> CardResponse:
        response = self._request("GET", Endpoints.CARD_BY_ID.format(card_id=card_id))
        return validate_card(parse_json(response))

    def update_card(self, card_id: str, payload: UpdateCardRequest) -> CardResponse:
        response = self._request(
            "PUT",
            Endpoints.CARD_BY_ID.format(card_id=card_id),
            params=payload.to_api_params(),
        )
        return validate_card(parse_json(response))

    def delete_card(self, card_id: str) -> requests.Response:
        return self._request("DELETE", Endpoints.CARD_BY_ID.format(card_id=card_id))

    def move_card(self, card_id: str, target_list_id: str) -> CardResponse:
        payload = UpdateCardRequest(id_list=target_list_id)
        return self.update_card(card_id, payload)

    def archive_card(self, card_id: str) -> CardResponse:
        payload = UpdateCardRequest(closed=True)
        return self.update_card(card_id, payload)

    def create_checklist(self, card_id: str, name: str) -> dict[str, Any]:
        response = self._request(
            "POST",
            Endpoints.CHECKLISTS,
            params={"name": name, "idCard": card_id},
        )
        return parse_json(response)

    def add_checkitem(self, checklist_id: str, name: str, checked: bool = False) -> dict[str, Any]:
        response = self._request(
            "POST",
            Endpoints.CHECKLIST_CHECK_ITEMS.format(checklist_id=checklist_id),
            params={"name": name, "checked": str(checked).lower()},
        )
        return parse_json(response)

    def get_member_boards(self) -> list[BoardResponse]:
        response = self._request("GET", Endpoints.MEMBERS_BOARDS)
        return validate_boards(parse_json(response))

    def get_workspaces(self) -> list[WorkspaceResponse]:
        response = self._request("GET", Endpoints.MEMBERS_ORGANIZATIONS)
        return validate_workspaces(parse_json(response))

    def raw_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        validate: bool = False,
    ) -> requests.Response:
        """Низкоуровневый запрос без валидации (для негативных сценариев)."""
        return self._request(method, path, params=params, validate=validate)
