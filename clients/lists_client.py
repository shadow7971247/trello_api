"""Lists business client."""

from __future__ import annotations

from clients.base_client import BaseClient
from models.request.create_list import CreateListRequest
from models.response.list_response import ListResponse


class ListsClient(BaseClient):
    def create_list(
        self,
        board_id: str,
        name: str,
        *,
        pos: str | float = "bottom",
    ) -> ListResponse:
        payload = CreateListRequest(name=name, id_board=board_id, pos=pos)
        return self.api.create_list(payload)

    def get_list(self, list_id: str) -> ListResponse:
        return self.api.get_list(list_id)

    def rename_list(self, list_id: str, name: str) -> ListResponse:
        return self.api.update_list(list_id, name=name)

