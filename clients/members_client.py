"""Members business client."""

from __future__ import annotations

from clients.base_client import BaseClient
from models.response.board_response import BoardResponse
from models.response.member_response import MemberResponse, WorkspaceResponse


class MembersClient(BaseClient):
    def get_current_user(self) -> MemberResponse:
        return self.api.get_current_user()

    def get_my_boards(self) -> list[BoardResponse]:
        return self.api.get_member_boards()

    def get_workspaces(self) -> list[WorkspaceResponse]:
        return self.api.get_workspaces()

