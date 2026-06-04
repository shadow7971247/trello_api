"""Модель ответа Trello API для доски."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BoardResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    url: str | None = None
    short_url: str | None = Field(default=None, alias="shortUrl")
    id_organization: str | None = Field(default=None, alias="idOrganization")
