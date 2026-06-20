"""Тесты чек-листов Trello API."""

from __future__ import annotations

import allure
import pytest

from api.client import TrelloApiClient
from fixtures.factories import prepare_checklist
from fixtures.generators import checkitem_name
from models.response.card_response import CardResponse


@allure.feature("Чек-листы")
@allure.story("Чек-листы и пункты проверки")
class TestChecklists:
    @allure.title("Создание чек-листа на карточке")
    @pytest.mark.checklists
    @pytest.mark.smoke
    def test_create_checklist(
        self,
        card: CardResponse,
        api_client: TrelloApiClient,
    ) -> None:
        with allure.step("Создание чек-листа"):
            checklist = prepare_checklist(api_client, card.id)

        with allure.step("Проверка полей чек-листа"):
            assert checklist["id"]
            assert checklist["name"]
            assert checklist["idCard"] == card.id

    @allure.title("Добавление пункта в чек-лист")
    @pytest.mark.checklists
    def test_add_checkitem(
        self,
        checklist: dict,
        api_client: TrelloApiClient,
    ) -> None:
        item_name = checkitem_name()

        with allure.step("Добавление пункта в чек-лист"):
            checkitem = api_client.add_checkitem(checklist["id"], item_name)

        with allure.step("Проверка созданного пункта"):
            assert checkitem["id"]
            assert checkitem["name"] == item_name
            assert checkitem["state"] in ("complete", "incomplete")
