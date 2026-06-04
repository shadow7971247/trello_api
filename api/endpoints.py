"""Константы эндпоинтов Trello REST API v1."""

from __future__ import annotations


class Endpoints:
    MEMBERS_ME = "/members/me"
    MEMBERS_BOARDS = "/members/me/boards"
    MEMBERS_ORGANIZATIONS = "/members/me/organizations"

    BOARDS = "/boards"
    BOARD_BY_ID = "/boards/{board_id}"
    BOARD_LISTS = "/boards/{board_id}/lists"

    LISTS = "/lists"
    LIST_BY_ID = "/lists/{list_id}"

    CARDS = "/cards"
    CARD_BY_ID = "/cards/{card_id}"

    CHECKLISTS = "/checklists"
    CHECKLIST_CHECK_ITEMS = "/checklists/{checklist_id}/checkItems"
