"""Генераторы тестовых данных для API-сущностей Trello."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from faker import Faker

from api.client import TrelloApiClient
from models.request.create_board import CreateBoardRequest
from models.request.create_card import CreateCardRequest
from models.request.create_list import CreateListRequest
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse

faker = Faker("ru_RU")


@dataclass
class EntityContext:
    """Контекст созданных сущностей для интеграции с UI/Mobile проектами."""

    board: BoardResponse | None = None
    trello_list: ListResponse | None = None
    card: CardResponse | None = None
    checklist: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "board_id": self.board.id if self.board else None,
            "board_name": self.board.name if self.board else None,
            "list_id": self.trello_list.id if self.trello_list else None,
            "list_name": self.trello_list.name if self.trello_list else None,
            "card_id": self.card.id if self.card else None,
            "card_name": self.card.name if self.card else None,
            "checklist_id": self.checklist.get("id") if self.checklist else None,
            **self.metadata,
        }


def board_name(prefix: str = "QA Board") -> str:
    return f"{prefix} {faker.uuid4()[:8]}"


def list_name(prefix: str = "QA List") -> str:
    return f"{prefix} {faker.word().capitalize()}"


def card_name(prefix: str = "QA Card") -> str:
    return f"{prefix} {faker.sentence(nb_words=3)}"


def card_description() -> str:
    return faker.paragraph(nb_sentences=2)


def checklist_name() -> str:
    return f"Checklist {faker.word().capitalize()}"


def checkitem_name() -> str:
    return faker.sentence(nb_words=4).rstrip(".")


def prepare_board(
    client: TrelloApiClient,
    name: str | None = None,
    *,
    permission_level: str = "private",
    desc: str | None = None,
) -> BoardResponse:
    payload = CreateBoardRequest(
        name=name or board_name(),
        desc=desc,
        prefs_permission_level=permission_level,
    )
    return client.create_board(payload)


def prepare_public_board(
    client: TrelloApiClient,
    name: str | None = None,
    *,
    desc: str | None = None,
) -> BoardResponse:
    """Публичная доска — доступна в UI без логина по прямому URL."""
    return prepare_board(client, name=name, permission_level="public", desc=desc)


def prepare_list(
    client: TrelloApiClient,
    board_id: str,
    name: str | None = None,
) -> ListResponse:
    payload = CreateListRequest(name=name or list_name(), id_board=board_id)
    return client.create_list(payload)


def prepare_card(
    client: TrelloApiClient,
    list_id: str,
    name: str | None = None,
    desc: str | None = None,
) -> CardResponse:
    payload = CreateCardRequest(
        name=name or card_name(),
        id_list=list_id,
        desc=desc or card_description(),
    )
    return client.create_card(payload)


def prepare_checklist(
    client: TrelloApiClient,
    card_id: str,
    name: str | None = None,
) -> dict[str, Any]:
    return client.create_checklist(card_id, name or checklist_name())
