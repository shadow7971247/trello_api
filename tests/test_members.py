"""Тесты участников и рабочих пространств Trello API."""

from __future__ import annotations

import allure
import pytest

from api.client import TrelloApiClient


@allure.feature("Участники")
@allure.story("Доски и рабочие пространства пользователя")
class TestMembers:
    @allure.title("Получение досок текущего участника")
    @pytest.mark.members
    @pytest.mark.smoke
    def test_get_member_boards(self, api_client: TrelloApiClient) -> None:
        with allure.step("Получение досок текущего участника (GET /members/me/boards)"):
            boards = api_client.get_member_boards()

        with allure.step("Проверка структуры ответа"):
            assert isinstance(boards, list)
            if boards:
                assert boards[0].id
                assert boards[0].name

    @allure.title("Получение рабочих пространств текущего участника")
    @pytest.mark.members
    def test_get_member_workspaces(self, api_client: TrelloApiClient) -> None:
        with allure.step("Получение рабочих пространств (GET /members/me/organizations)"):
            workspaces = api_client.get_workspaces()

        with allure.step("Проверка структуры ответа"):
            assert isinstance(workspaces, list)
            if workspaces:
                assert workspaces[0].id
                assert workspaces[0].name
