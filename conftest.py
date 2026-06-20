"""Глобальные pytest-фикстуры проекта."""

from __future__ import annotations

from collections.abc import Generator

import allure
import pytest

from api.client import TrelloApiClient
from fixtures.factories import prepare_board, prepare_card, prepare_checklist, prepare_list, prepare_public_board
from fixtures.generators import board_name
from fixtures.test_data import BOARD_NAME_PREFIX
from models.request.create_board import CreateBoardRequest
from models.response.board_response import BoardResponse
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse
from utils.attach import attach_text
from utils.config import Config


@pytest.fixture(scope="session")
def app_config() -> Config:
    config = Config.from_env()
    config.validate()
    return config


@pytest.fixture(scope="session")
def base_url(app_config: Config) -> str:
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
def public_board(api_client: TrelloApiClient) -> Generator[BoardResponse, None, None]:
    created = prepare_public_board(api_client)
    yield created
    api_client.delete_board(created.id)


@pytest.fixture
def created_board(api_client: TrelloApiClient) -> Generator[tuple[str, BoardResponse], None, None]:
    name = board_name(BOARD_NAME_PREFIX)
    board = api_client.create_board(CreateBoardRequest(name=name))
    yield name, board
    api_client.delete_board(board.id)


@pytest.fixture
def created_public_board(api_client: TrelloApiClient) -> Generator[BoardResponse, None, None]:
    board = prepare_public_board(api_client)
    yield board
    api_client.delete_board(board.id)


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
def created_card(
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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    if report.when == "setup":
        allure.dynamic.epic("Trello API")
    if report.when != "call":
        return
    attach_text(
        "Результат",
        f"{item.name}: {report.outcome} ({report.duration:.2f} с)",
    )
