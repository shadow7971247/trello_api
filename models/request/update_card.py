"""Модель запроса на обновление карточки."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UpdateCardRequest(BaseModel):
    name: str | None = Field(default=None, description="Новое название")
    desc: str | None = Field(default=None, description="Новое описание")
    id_list: str | None = Field(default=None, alias="idList", description="ID целевого списка")
    closed: bool | None = Field(default=None, description="Архивировать карточку")

    model_config = {"populate_by_name": True}

    def to_api_params(self) -> dict[str, str | bool]:
        params: dict[str, str | bool] = {}
        if self.name is not None:
            params["name"] = self.name
        if self.desc is not None:
            params["desc"] = self.desc
        if self.id_list is not None:
            params["idList"] = self.id_list
        if self.closed is not None:
            params["closed"] = str(self.closed).lower()
        return params
