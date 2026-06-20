"""Операции с карточками."""

from __future__ import annotations

import requests

from api.assertions import assert_status_code
from api.endpoints import Endpoints
from api.helpers import parse_json
from api.http import HttpClient
from api.validators import validate_card
from models.request.create_card import CreateCardRequest
from models.request.update_card import UpdateCardRequest
from models.response.card_response import CardResponse


class CardsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, payload: CreateCardRequest) -> CardResponse:
        response = self._http.request("POST", Endpoints.CARDS, params=payload.to_api_params())
        assert_status_code(response, 200)
        return validate_card(parse_json(response))

    def get(self, card_id: str) -> CardResponse:
        response = self._http.request("GET", Endpoints.CARD_BY_ID.format(card_id=card_id))
        assert_status_code(response, 200)
        return validate_card(parse_json(response))

    def update(self, card_id: str, payload: UpdateCardRequest) -> CardResponse:
        response = self._http.request(
            "PUT",
            Endpoints.CARD_BY_ID.format(card_id=card_id),
            params=payload.to_api_params(),
        )
        assert_status_code(response, 200)
        return validate_card(parse_json(response))

    def delete(self, card_id: str) -> requests.Response:
        response = self._http.request("DELETE", Endpoints.CARD_BY_ID.format(card_id=card_id))
        assert_status_code(response, 200)
        return response

    def move(self, card_id: str, target_list_id: str) -> CardResponse:
        payload = UpdateCardRequest(id_list=target_list_id)
        return self.update(card_id, payload)

    def archive(self, card_id: str) -> CardResponse:
        payload = UpdateCardRequest(closed=True)
        return self.update(card_id, payload)
