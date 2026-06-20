"""Тесты досок Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import assert_equals, assert_status_code
from api.client import TrelloApiClient
from api.endpoints import Endpoints
from fixtures.generators import board_name
from fixtures.test_data import BOARD_NAME_PREFIX
from models.request.create_board import CreateBoardRequest
from models.response.board_response import BoardResponse


@allure.feature("Доски")
@allure.story("CRUD операции с досками")
class TestBoards:
    @allure.title("Создание доски")
    @pytest.mark.boards
    @pytest.mark.smoke
    def test_create_board(self, created_board: tuple[str, BoardResponse]) -> None:
        name, board = created_board
        with allure.step("Проверка полей созданной доски"):
            assert board.id
            assert_equals(board.name, name, "board.name")

    @allure.title("Получение доски по ID")
    @pytest.mark.boards
    def test_get_board(self, board: BoardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("Получение доски по ID"):
            fetched = api_client.get_board(board.id)

        with allure.step("Проверка соответствия данных"):
            assert_equals(fetched.id, board.id, "board.id")
            assert_equals(fetched.name, board.name, "board.name")

    @allure.title("Обновление названия доски")
    @pytest.mark.boards
    def test_update_board(self, board: BoardResponse, api_client: TrelloApiClient) -> None:
        new_name = board_name("Updated Board")

        with allure.step("Обновление названия доски"):
            updated = api_client.update_board(board.id, name=new_name)

        with allure.step("Проверка обновлённого имени"):
            assert_equals(updated.name, new_name, "board.name")

    @allure.title("Удаление доски")
    @pytest.mark.boards
    def test_delete_board(self, api_client: TrelloApiClient) -> None:
        from fixtures.factories import prepare_board

        board = prepare_board(api_client)
        board_id = board.id

        with allure.step("Удаление доски"):
            api_client.delete_board(board_id)

        with allure.step("Проверка недоступности удалённой доски"):
            response = api_client.raw_request(
                "GET",
                Endpoints.BOARD_BY_ID.format(board_id=board_id),
            )
            assert_status_code(response, 404)

    @allure.title("Создание публичной доски")
    @pytest.mark.boards
    @pytest.mark.smoke
    def test_create_public_board(self, created_public_board: BoardResponse) -> None:
        with allure.step("Проверка URL и shortUrl"):
            assert created_public_board.url
            assert created_public_board.short_url
            assert created_public_board.url.startswith("https://")

    @allure.title("Закрытие (архивация) доски через API")
    @pytest.mark.boards
    def test_close_board(self, api_client: TrelloApiClient, board: BoardResponse) -> None:
        with allure.step("Архивирование доски (closed=true)"):
            closed = api_client.close_board(board.id)

        with allure.step("Проверка флага архивации"):
            assert_equals(closed.closed, True, "board.closed")
            fetched = api_client.get_board(board.id)
            assert_equals(fetched.closed, True, "board.closed")

    @allure.title("Ошибка при создании доски без имени")
    @pytest.mark.boards
    def test_create_board_without_name(self, api_client: TrelloApiClient) -> None:
        with allure.step("Создание доски без обязательного поля name"):
            response = api_client.raw_request(
                "POST",
                Endpoints.BOARDS,
                params={"defaultLists": "false"},
            )

        with allure.step("Проверка статуса 400"):
            assert_status_code(response, 400)
