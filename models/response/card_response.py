"""Модель ответа Trello API для карточки."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CardResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    desc: str | None = None
    closed: bool = False
    id_list: str = Field(alias="idList")
    id_board: str | None = Field(default=None, alias="idBoard")
    url: str | None = None
    short_url: str | None = Field(default=None, alias="shortUrl")
    pos: float | None = None
