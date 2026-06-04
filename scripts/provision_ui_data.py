#!/usr/bin/env python
"""CLI: создать тестовые сущности Trello и сохранить artifacts/test-context.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.client import TrelloApiClient
from fixtures.ui_provision import provision_ui_test_data
from utils.config import config


def main() -> int:
    config.validate()
    client = TrelloApiClient(config)
    payload = provision_ui_test_data(client)

    board_url = payload.get("board_url") or payload.get("board_short_url")
    print("UI test data created and verified.")
    print(f"  Context file: {payload['_context_file']}")
    print(f"  Board:        {payload['board_name']}")
    print(f"  Open board:   {board_url}")
    print(f"  Card:         {payload['card_name']}")
    print(f"  All boards:   {payload.get('trello_boards_url')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
