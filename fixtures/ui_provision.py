"""Создание и удаление тестовых данных Trello для UI-проверок."""

from __future__ import annotations

from typing import Any

from api.assertions import (
    assert_board_name,
    assert_card_description,
    assert_card_in_list,
    assert_card_name,
    assert_list_name,
)
from api.client import TrelloApiClient
from fixtures.generators import (
    EntityContext,
    board_name,
    card_description,
    card_name,
    checkitem_name,
    checklist_name,
    list_name,
    prepare_board,
    prepare_card,
    prepare_checklist,
    prepare_list,
)
from fixtures.test_data import BOARD_NAME_PREFIX, CARD_NAME_PREFIX, LIST_NAME_PREFIX
from utils.test_context import (
    CONTEXT_FILE,
    load_test_context,
    remove_test_context_file,
    save_test_context,
)


def build_export_payload(
    ctx: EntityContext,
    *,
    checkitem: dict[str, Any] | None = None,
    member_username: str | None = None,
) -> dict[str, Any]:
    board = ctx.board
    trello_list = ctx.trello_list
    card = ctx.card
    checklist = ctx.checklist

    payload: dict[str, Any] = {
        "board_id": board.id if board else None,
        "board_name": board.name if board else None,
        "board_url": board.url if board else None,
        "board_short_url": board.short_url if board else None,
        "list_id": trello_list.id if trello_list else None,
        "list_name": trello_list.name if trello_list else None,
        "card_id": card.id if card else None,
        "card_name": card.name if card else None,
        "card_desc": card.desc if card else None,
        "card_url": card.url if card else None,
        "card_short_url": card.short_url if card else None,
        "checklist_id": checklist.get("id") if checklist else None,
        "checklist_name": checklist.get("name") if checklist else None,
        "checkitem_id": checkitem.get("id") if checkitem else None,
        "checkitem_name": checkitem.get("name") if checkitem else None,
        "member_username": member_username,
        "trello_boards_url": (
            f"https://trello.com/{member_username}/boards"
            if member_username
            else "https://trello.com"
        ),
    }
    payload.update(ctx.metadata)
    return payload


def verify_stack(client: TrelloApiClient, ctx: EntityContext) -> None:
    assert ctx.board is not None
    assert ctx.trello_list is not None
    assert ctx.card is not None

    fetched_board = client.get_board(ctx.board.id)
    assert_board_name(fetched_board, ctx.board.name)

    fetched_list = client.get_list(ctx.trello_list.id)
    assert_list_name(fetched_list, ctx.trello_list.name)

    fetched_card = client.get_card(ctx.card.id)
    assert_card_name(fetched_card, ctx.card.name)
    if ctx.card.desc:
        assert_card_description(fetched_card, ctx.card.desc)
    assert_card_in_list(fetched_card, ctx.trello_list.id)


def _cleanup_board_if_present(client: TrelloApiClient, board_id: str | None) -> None:
    if not board_id:
        return
    response = client.delete_board(board_id)
    if response.status_code not in (200, 404, 410):
        response.raise_for_status()


def provision_ui_test_data(client: TrelloApiClient) -> dict[str, Any]:
    """Создаёт полный набор сущностей, проверяет через API, сохраняет JSON."""
    if CONTEXT_FILE.is_file():
        previous = load_test_context()
        _cleanup_board_if_present(client, previous.get("board_id"))

    member = client.get_current_user()
    username = member.username

    board = prepare_board(client, name=board_name(BOARD_NAME_PREFIX))
    trello_list = prepare_list(client, board.id, name=list_name(LIST_NAME_PREFIX))
    desc = card_description()
    card = prepare_card(
        client,
        trello_list.id,
        name=card_name(CARD_NAME_PREFIX),
        desc=desc,
    )
    checklist = prepare_checklist(client, card.id, name=checklist_name())
    checkitem = client.add_checkitem(checklist["id"], checkitem_name())

    ctx = EntityContext(
        board=board,
        trello_list=trello_list,
        card=card,
        checklist=checklist,
        metadata={"checkitem_id": checkitem.get("id")},
    )
    verify_stack(client, ctx)

    payload = build_export_payload(ctx, checkitem=checkitem, member_username=username)
    path = save_test_context(payload)
    payload["_context_file"] = str(path)
    return payload


def cleanup_ui_test_data(client: TrelloApiClient) -> None:
    """Удаляет ресурсы по сохранённому контексту и убирает JSON."""
    data = load_test_context()
    _cleanup_board_if_present(client, data.get("board_id"))
    remove_test_context_file()
