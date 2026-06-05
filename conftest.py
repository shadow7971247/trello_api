"""Глобальные pytest-фикстуры проекта."""

from __future__ import annotations

from collections.abc import Generator

import pytest

from api.client import TrelloApiClient
from fixtures.generators import (
    prepare_board,
    prepare_card,
    prepare_checklist,
    prepare_list,
)
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from utils.config import Config, config

@pytest.fixture(scope="session")
def app_config() -> Config:
    config.validate()
    return config


@pytest.fixture(scope="session")
def base_url(app_config: Config) -> str:
    """Базовый URI Trello API."""
    return app_config.base_url


@pytest.fixture(scope="session")
def api_client(app_config: Config) -> TrelloApiClient:
    return TrelloApiClient(app_config)


@pytest.fixture
def board(api_client: TrelloApiClient) -> Generator[BoardResponse, None, None]:
    created = prepare_board(api_client)
    yield created
    api_client.delete_board(created.id)


@pytest.fixture
def trello_list(
    api_client: TrelloApiClient,
    board: BoardResponse,
) -> Generator[ListResponse, None, None]:
    created = prepare_list(api_client, board.id)
    yield created


@pytest.fixture
def card(
    api_client: TrelloApiClient,
    trello_list: ListResponse,
) -> Generator[CardResponse, None, None]:
    created = prepare_card(api_client, trello_list.id)
    yield created
    api_client.delete_card(created.id)


@pytest.fixture
def second_list(
    api_client: TrelloApiClient,
    board: BoardResponse,
) -> Generator[ListResponse, None, None]:
    created = prepare_list(api_client, board.id)
    yield created


@pytest.fixture
def checklist(
    api_client: TrelloApiClient,
    card: CardResponse,
) -> Generator[dict, None, None]:
    created = prepare_checklist(api_client, card.id)
    yield created
