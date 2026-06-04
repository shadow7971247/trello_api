"""Модели ответа Trello API для участника и рабочего пространства."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MemberResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    username: str | None = None
    full_name: str | None = Field(default=None, alias="fullName")
    url: str | None = None


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    display_name: str | None = Field(default=None, alias="displayName")
    url: str | None = None
