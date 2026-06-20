"""Операции с участником и workspace."""

from __future__ import annotations

from api.assertions import assert_status_code
from api.endpoints import Endpoints
from api.helpers import parse_json
from api.http import HttpClient
from api.validators import validate_member, validate_workspaces
from models.response.member_response import MemberResponse, WorkspaceResponse


class MembersClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_current(self) -> MemberResponse:
        response = self._http.request("GET", Endpoints.MEMBERS_ME)
        assert_status_code(response, 200)
        return validate_member(parse_json(response))

    def get_workspaces(self) -> list[WorkspaceResponse]:
        response = self._http.request("GET", Endpoints.MEMBERS_ORGANIZATIONS)
        assert_status_code(response, 200)
        return validate_workspaces(parse_json(response))
