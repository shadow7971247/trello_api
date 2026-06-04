"""Cards business client."""

from __future__ import annotations

import requests

from clients.base_client import BaseClient
from models.request.create_card import CreateCardRequest
from models.request.update_card import UpdateCardRequest
from models.response.card_response import CardResponse


class CardsClient(BaseClient):
    def create_card(
        self,
        list_id: str,
        name: str,
        *,
        desc: str | None = None,
        pos: str | float = "bottom",
    ) -> CardResponse:
        payload = CreateCardRequest(name=name, id_list=list_id, desc=desc, pos=pos)
        return self.api.create_card(payload)

    def get_card(self, card_id: str) -> CardResponse:
        return self.api.get_card(card_id)

    def update_card(
        self,
        card_id: str,
        *,
        name: str | None = None,
        desc: str | None = None,
    ) -> CardResponse:
        payload = UpdateCardRequest(name=name, desc=desc)
        return self.api.update_card(card_id, payload)

    def move_card(self, card_id: str, target_list_id: str) -> CardResponse:
        return self.api.move_card(card_id, target_list_id)

    def archive_card(self, card_id: str) -> CardResponse:
        return self.api.archive_card(card_id)

    def delete_card(self, card_id: str) -> requests.Response:
        return self.api.delete_card(card_id)

