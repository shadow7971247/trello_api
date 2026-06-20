"""Тесты аутентификации Trello API."""

from __future__ import annotations

import allure
import pytest

from api.assertions import assert_status_code
from api.client import TrelloApiClient
from api.endpoints import Endpoints
from fixtures.test_data import INVALID_TOKEN
from utils.config import Config


@allure.feature("Аутентификация")
@allure.story("Текущий пользователь")
class TestAuth:
    @allure.title("Получение текущего пользователя по валидному токену")
    @pytest.mark.auth
    @pytest.mark.smoke
    def test_get_current_user(self, api_client: TrelloApiClient) -> None:
        with allure.step("Запрос GET /members/me"):
            member = api_client.get_current_user()

        with allure.step("Проверка обязательных полей пользователя"):
            assert member.id
            assert member.username or member.full_name

    @allure.title("Ошибка при невалидном API-токене")
    @pytest.mark.auth
    def test_invalid_token(self, app_config: Config) -> None:
        invalid_config = Config(
            base_url=app_config.base_url,
            api_key=app_config.api_key,
            api_token=INVALID_TOKEN,
        )
        client = TrelloApiClient(invalid_config)

        with allure.step("Запрос с невалидным токеном"):
            response = client.raw_request("GET", Endpoints.MEMBERS_ME)

        with allure.step("Проверка статуса 401"):
            assert_status_code(response, 401)
