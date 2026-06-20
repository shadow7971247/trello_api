"""Чек-листы и пункты чек-листа."""

from __future__ import annotations

from typing import Any

from api.assertions import assert_status_code
from api.endpoints import Endpoints
from api.helpers import parse_json
from api.http import HttpClient


class ChecklistsClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, card_id: str, name: str) -> dict[str, Any]:
        response = self._http.request(
            "POST",
            Endpoints.CHECKLISTS,
            params={"name": name, "idCard": card_id},
        )
        assert_status_code(response, 200)
        return parse_json(response)

    def add_item(self, checklist_id: str, name: str, checked: bool = False) -> dict[str, Any]:
        response = self._http.request(
            "POST",
            Endpoints.CHECKLIST_CHECK_ITEMS.format(checklist_id=checklist_id),
            params={"name": name, "checked": str(checked).lower()},
        )
        assert_status_code(response, 200)
        return parse_json(response)
