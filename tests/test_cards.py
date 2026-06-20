"""Тесты карточек Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import assert_equals, assert_status_code
from api.client import TrelloApiClient
from api.endpoints import Endpoints
from fixtures.generators import card_description, card_name
from fixtures.test_data import CARD_NAME_PREFIX
from models.request.update_card import UpdateCardRequest
from models.response.card_response import CardResponse
from models.response.list_response import ListResponse


@allure.feature("Карточки")
@allure.story("CRUD и перемещение карточек")
class TestCards:
    @allure.title("Создание карточки в списке")
    @pytest.mark.cards
    @pytest.mark.smoke
    def test_create_card(
        self,
        created_card: CardResponse,
        trello_list: ListResponse,
    ) -> None:
        with allure.step("Проверка полей карточки"):
            assert created_card.id
            assert_equals(created_card.id_list, trello_list.id, "card.id_list")

    @allure.title("Получение карточки по ID")
    @pytest.mark.cards
    def test_get_card(self, card: CardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("Получение карточки по ID"):
            fetched = api_client.get_card(card.id)

        with allure.step("Проверка данных карточки"):
            assert_equals(fetched.id, card.id, "card.id")
            assert_equals(fetched.name, card.name, "card.name")

    @allure.title("Переименование карточки")
    @pytest.mark.cards
    def test_rename_card(self, card: CardResponse, api_client: TrelloApiClient) -> None:
        new_name = card_name("Renamed")

        with allure.step("Обновление названия карточки"):
            updated = api_client.update_card(card.id, UpdateCardRequest(name=new_name))

        with allure.step("Проверка нового имени"):
            assert_equals(updated.name, new_name, "card.name")

    @allure.title("Обновление описания карточки")
    @pytest.mark.cards
    def test_update_card_description(
        self,
        card: CardResponse,
        api_client: TrelloApiClient,
    ) -> None:
        new_desc = card_description()

        with allure.step("Обновление описания карточки"):
            updated = api_client.update_card(card.id, UpdateCardRequest(desc=new_desc))

        with allure.step("Проверка описания"):
            assert_equals(updated.desc, new_desc, "card.desc")

    @allure.title("Перемещение карточки между списками")
    @pytest.mark.cards
    def test_move_card_between_lists(
        self,
        card: CardResponse,
        second_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        with allure.step("Перемещение карточки в другой список"):
            moved = api_client.move_card(card.id, second_list.id)

        with allure.step("Проверка idList после перемещения"):
            assert_equals(moved.id_list, second_list.id, "card.id_list")

    @allure.title("Архивирование карточки")
    @pytest.mark.cards
    def test_archive_card(self, card: CardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("Архивирование карточки (closed=true)"):
            archived = api_client.archive_card(card.id)

        with allure.step("Проверка флага архивации"):
            assert_equals(archived.closed, True, "card.closed")

    @allure.title("Удаление карточки")
    @pytest.mark.cards
    def test_delete_card(
        self,
        trello_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        from fixtures.factories import prepare_card

        card = prepare_card(api_client, trello_list.id)
        card_id = card.id

        with allure.step("Удаление карточки"):
            api_client.delete_card(card_id)

        with allure.step("Проверка отсутствия карточки"):
            response = api_client.raw_request("GET", Endpoints.CARD_BY_ID.format(card_id=card_id))
            assert_status_code(response, 404)
