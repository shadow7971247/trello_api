"""Модель запроса на создание карточки."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCardRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Название карточки")
    id_list: str = Field(..., alias="idList", description="ID списка")
    desc: str | None = Field(default=None, description="Описание карточки")
    pos: str | float = Field(default="bottom", description="Позиция в списке")

    model_config = {"populate_by_name": True}

    def to_api_params(self) -> dict[str, str | float]:
        params: dict[str, str | float] = {
            "name": self.name,
            "idList": self.id_list,
            "pos": self.pos,
        }
        if self.desc is not None:
            params["desc"] = self.desc
        return params
