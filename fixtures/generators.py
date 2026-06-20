"""Генераторы имён и текстов для тестовых данных."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from faker import Faker

from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse

faker = Faker("ru_RU")


@dataclass
class EntityContext:
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
