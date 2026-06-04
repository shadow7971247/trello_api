"""Тесты карточек Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import (
    assert_card_closed,
    assert_card_description,
    assert_card_in_list,
    assert_card_name,
    assert_status_code,
)
from api.client import TrelloApiClient
from fixtures.generators import card_description, card_name, prepare_card
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
        trello_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        name = card_name(CARD_NAME_PREFIX)

        with allure.step("Создание карточки"):
            created = prepare_card(api_client, trello_list.id, name=name)

        try:
            with allure.step("Проверка полей карточки"):
                assert created.id
                assert_card_name(created, name)
                assert_card_in_list(created, trello_list.id)
        finally:
            api_client.delete_card(created.id)

    @allure.title("Получение карточки по ID")
    @pytest.mark.cards
    def test_get_card(self, card: CardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("GET карточки по ID"):
            fetched = api_client.get_card(card.id)

        with allure.step("Проверка данных карточки"):
            assert fetched.id == card.id
            assert_card_name(fetched, card.name)

    @allure.title("Обновление описания карточки")
    @pytest.mark.cards
    def test_update_card_description(
        self,
        card: CardResponse,
        api_client: TrelloApiClient,
    ) -> None:
        new_desc = card_description()

        with allure.step("PUT обновление описания"):
            updated = api_client.update_card(
                card.id,
                UpdateCardRequest(desc=new_desc),
            )

        with allure.step("Проверка описания"):
            assert_card_description(updated, new_desc)

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
            assert_card_in_list(moved, second_list.id)

    @allure.title("Архивирование карточки")
    @pytest.mark.cards
    def test_archive_card(self, card: CardResponse, api_client: TrelloApiClient) -> None:
        with allure.step("Архивирование карточки (closed=true)"):
            archived = api_client.archive_card(card.id)

        with allure.step("Проверка статуса closed"):
            assert_card_closed(archived, closed=True)

    @allure.title("Удаление карточки")
    @pytest.mark.cards
    def test_delete_card(
        self,
        trello_list: ListResponse,
        api_client: TrelloApiClient,
    ) -> None:
        created = prepare_card(api_client, trello_list.id)

        with allure.step("DELETE карточки"):
            response = api_client.delete_card(created.id)
            assert_status_code(response, 200)

        with allure.step("Проверка отсутствия карточки"):
            get_response = api_client.raw_request(
                "GET",
                f"/cards/{created.id}",
                validate=False,
            )
            assert get_response.status_code in (404, 410)
