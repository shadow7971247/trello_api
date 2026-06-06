"""Тесты досок Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import assert_board_name, assert_status_code
from api.client import TrelloApiClient
from api.endpoints import Endpoints
from fixtures.generators import board_name, prepare_board
from fixtures.test_data import BOARD_NAME_PREFIX
from models.request.create_board import CreateBoardRequest
from models.response.board_response import BoardResponse


@allure.feature("Доски")
@allure.story("CRUD операции с досками")
class TestBoards:
    @allure.title("Создание доски")
    @pytest.mark.boards
    @pytest.mark.smoke
    def test_create_board(self, api_client: TrelloApiClient) -> None:
        name = board_name(BOARD_NAME_PREFIX)
        payload = CreateBoardRequest(name=name)

        with allure.step("Создание доски через API"):
            board = api_client.create_board(payload)

        try:
            with allure.step("Проверка полей созданной доски"):
                assert board.id
                assert_board_name(board, name)
        finally:
            api_client.delete_board(board.id)

    @allure.title("Получение доски по ID")
    @pytest.mark.boards
    def test_get_board(self, board: BoardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("Получение доски по ID"):
            fetched = api_client.get_board(board.id)

        with allure.step("Проверка соответствия данных"):
            assert fetched.id == board.id
            assert_board_name(fetched, board.name)

    @allure.title("Обновление названия доски")
    @pytest.mark.boards
    def test_update_board(self, board: BoardResponse, api_client: TrelloApiClient) -> None:
        new_name = board_name("Updated Board")

        with allure.step("Обновление названия доски"):
            updated = api_client.update_board(board.id, name=new_name)

        with allure.step("Проверка обновлённого имени"):
            assert_board_name(updated, new_name)

    @allure.title("Удаление доски")
    @pytest.mark.boards
    def test_delete_board(self, api_client: TrelloApiClient) -> None:
        board = prepare_board(api_client)

        with allure.step("Удаление доски"):
            response = api_client.delete_board(board.id)
            assert_status_code(response, 200)

        with allure.step("Проверка недоступности удалённой доски"):
            get_response = api_client.raw_request(
                "GET",
                Endpoints.BOARD_BY_ID.format(board_id=board.id),
                validate=False,
            )
            assert get_response.status_code in (404, 410)

    @allure.title("Создание публичной доски")
    @pytest.mark.boards
    @pytest.mark.smoke
    def test_create_public_board(self, api_client: TrelloApiClient) -> None:
        name = board_name("Public Board")
        payload = CreateBoardRequest(
            name=name,
            prefs_permission_level="public",
            desc="Public board for anonymous UI checks",
        )

        with allure.step("Создание публичной доски"):
            board = api_client.create_board(payload)

        try:
            with allure.step("Проверка URL и короткой ссылки"):
                assert board.url
                assert board.short_url
                assert board.url.startswith("https://")
        finally:
            api_client.delete_board(board.id)

    @allure.title("Закрытие (архивация) доски через API")
    @pytest.mark.boards
    def test_close_board(self, api_client: TrelloApiClient) -> None:
        board = prepare_board(api_client)

        with allure.step("Архивирование доски (closed=true)"):
            closed = api_client.close_board(board.id)

        with allure.step("Проверка флага архивации"):
            assert closed.closed is True
            fetched = api_client.get_board(board.id)
            assert fetched.closed is True

        api_client.delete_board(board.id)

    @allure.title("Ошибка при создании доски без имени")
    @pytest.mark.boards
    def test_create_board_without_name(self, api_client: TrelloApiClient) -> None:
        with allure.step("Создание доски без обязательного поля name"):
            response = api_client.raw_request(
                "POST",
                Endpoints.BOARDS,
                params={"defaultLists": "false"},
                validate=False,
            )

        with allure.step("Проверка статуса 400"):
            assert_status_code(response, 400)
