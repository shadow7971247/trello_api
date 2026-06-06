"""Подготовка и очистка данных Trello для UI-тестов (отдельный репозиторий)."""

from __future__ import annotations

import allure
import pytest

from api.client import TrelloApiClient
from fixtures.ui_provision import cleanup_ui_test_data, provision_ui_test_data


@allure.feature("Провайдер данных для UI")
@allure.story("Подготовка данных для Selenium")
class TestUiProvision:
    @allure.title("Создать и проверить сущности для UI, сохранить test-context.json")
    @pytest.mark.ui_setup
    def test_provision_ui_test_data(self, api_client: TrelloApiClient) -> None:
        with allure.step("Создание цепочки: доска → список → карточка → чек-лист → пункт"):
            payload = provision_ui_test_data(api_client)

        with allure.step("Проверка сохранённого контекста"):
            assert payload["board_id"]
            assert payload["board_url"] or payload["board_short_url"]
            assert payload["list_id"]
            assert payload["card_id"]
            assert payload["checklist_id"]
            assert payload["_context_file"]

    @allure.title("Удалить сущности UI-тестов по test-context.json")
    @pytest.mark.ui_teardown
    def test_cleanup_ui_test_data(self, api_client: TrelloApiClient) -> None:
        with allure.step("Удаление доски и очистка файла test-context.json"):
            cleanup_ui_test_data(api_client)
