"""Тесты списков Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import assert_equals
from api.client import TrelloApiClient
from fixtures.factories import prepare_list
from fixtures.generators import list_name
from fixtures.test_data import LIST_NAME_PREFIX
from models.response.board_response import BoardResponse
from models.response.list_response import ListResponse


@allure.feature("Списки")
@allure.story("CRUD операции со списками")
class TestLists:
    @allure.title("Создание списка на доске")
    @pytest.mark.lists
    @pytest.mark.smoke
    def test_create_list(
        self,
        board: BoardResponse,
        api_client: TrelloApiClient,
    ) -> None:
        name = list_name(LIST_NAME_PREFIX)

        with allure.step("Создание списка"):
            created = prepare_list(api_client, board.id, name=name)

        with allure.step("Проверка полей списка"):
            assert created.id
            assert_equals(created.name, name, "list.name")
            assert_equals(created.id_board, board.id, "list.id_board")

    @allure.title("Получение списка по ID")
    @pytest.mark.lists
    def test_get_list(
        self,
        trello_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        with allure.step("Получение списка по ID"):
            fetched = api_client.get_list(trello_list.id)

        with allure.step("Проверка данных списка"):
            assert_equals(fetched.id, trello_list.id, "list.id")
            assert_equals(fetched.name, trello_list.name, "list.name")

    @allure.title("Переименование списка")
    @pytest.mark.lists
    def test_rename_list(
        self,
        trello_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        new_name = list_name("Renamed List")

        with allure.step("Переименование списка"):
            updated = api_client.update_list(trello_list.id, name=new_name)

        with allure.step("Проверка нового имени"):
            assert_equals(updated.name, new_name, "list.name")
