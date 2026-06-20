"""Операции со списками."""

from __future__ import annotations

from api.assertions import assert_status_code
from api.endpoints import Endpoints
from api.helpers import parse_json
from api.http import HttpClient
from api.validators import validate_list
from models.request.create_list import CreateListRequest
from models.response.list_response import ListResponse


class ListsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, payload: CreateListRequest) -> ListResponse:
        response = self._http.request("POST", Endpoints.LISTS, params=payload.to_api_params())
        assert_status_code(response, 200)
        return validate_list(parse_json(response))

    def get(self, list_id: str) -> ListResponse:
        response = self._http.request("GET", Endpoints.LIST_BY_ID.format(list_id=list_id))
        assert_status_code(response, 200)
        return validate_list(parse_json(response))

    def update(self, list_id: str, *, name: str) -> ListResponse:
        response = self._http.request(
            "PUT",
            Endpoints.LIST_BY_ID.format(list_id=list_id),
            params={"name": name},
        )
        assert_status_code(response, 200)
        return validate_list(parse_json(response))
