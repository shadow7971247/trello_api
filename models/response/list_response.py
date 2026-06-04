"""Модель ответа Trello API для списка."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    closed: bool = False
    id_board: str = Field(alias="idBoard")
    pos: float | None = None
