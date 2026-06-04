#!/usr/bin/env python
"""CLI: удалить сущности Trello по artifacts/test-context.json."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.client import TrelloApiClient
from fixtures.ui_provision import cleanup_ui_test_data
from utils.config import config


def main() -> int:
    config.validate()
    client = TrelloApiClient(config)
    cleanup_ui_test_data(client)
    print("UI test data removed. artifacts/test-context.json deleted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
