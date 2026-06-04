"""Модель запроса на создание списка."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateListRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Название списка")
    id_board: str = Field(..., alias="idBoard", description="ID доски")
    pos: str | float = Field(default="bottom", description="Позиция в доске")

    model_config = {"populate_by_name": True}

    def to_api_params(self) -> dict[str, str | float]:
        return {"name": self.name, "idBoard": self.id_board, "pos": self.pos}
