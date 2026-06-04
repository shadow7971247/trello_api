"""Модель запроса на создание доски."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CreateBoardRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Название доски")
    desc: str | None = Field(default=None, description="Описание доски")
    default_lists: bool = Field(default=False, alias="defaultLists")
    prefs_permission_level: str = Field(default="private", alias="prefs_permissionLevel")

    model_config = {"populate_by_name": True}

    def to_api_params(self) -> dict[str, str | bool]:
        params: dict[str, str | bool] = {
            "name": self.name,
            "defaultLists": str(self.default_lists).lower(),
        }
        if self.desc is not None:
            params["desc"] = self.desc
        params["prefs_permissionLevel"] = self.prefs_permission_level
        return params
