"""Public config API for trello_api.

UI/Mobile repositories can import configuration from here:
`from trello_api.config import config, Config`.
"""

from __future__ import annotations

from utils.config import Config, config

__all__ = ["Config", "config"]

