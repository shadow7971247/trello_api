"""Слой проверок для API-тестов."""

from __future__ import annotations

import requests

from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse


def assert_status_code(response: requests.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"Ожидался статус {expected}, получен {response.status_code}. "
        f"Тело ответа: {response.text}"
    )


def assert_board_name(board: BoardResponse, expected_name: str) -> None:
    assert board.name == expected_name, (
        f"Ожидалось имя доски '{expected_name}', получено '{board.name}'"
    )


def assert_list_name(trello_list: ListResponse, expected_name: str) -> None:
    assert trello_list.name == expected_name, (
        f"Ожидалось имя списка '{expected_name}', получено '{trello_list.name}'"
    )


def assert_card_name(card: CardResponse, expected_name: str) -> None:
    assert card.name == expected_name, (
        f"Ожидалось имя карточки '{expected_name}', получено '{card.name}'"
    )


def assert_card_description(card: CardResponse, expected_description: str) -> None:
    assert card.desc == expected_description, (
        f"Ожидалось описание '{expected_description}', получено '{card.desc}'"
    )


def assert_card_in_list(card: CardResponse, list_id: str) -> None:
    assert card.id_list == list_id, (
        f"Карточка должна быть в списке {list_id}, но находится в {card.id_list}"
    )


def assert_card_closed(card: CardResponse, closed: bool = True) -> None:
    assert card.closed is closed, (
        f"Ожидался closed={closed}, получено closed={card.closed}"
    )
