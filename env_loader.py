"""Загрузка .env: trello_ui/.env (общие Trello/API), затем trello_api/.env."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent
_SHARED_UI_ENV = _PROJECT_ROOT.parent / "trello_ui" / ".env"

load_dotenv(_SHARED_UI_ENV)
load_dotenv(_PROJECT_ROOT / ".env", override=True)
