"""
Majority of library contained within subsequent ``snowmobile.core`` modules;
buried in ``core`` to keep from cluttering intellisense/auto-complete
recommendations when interacting with ``snowmobile`` objects.
"""
__all__ = [
    "Configuration",
    "Connector",
    "Connect",
    "Loader",
    "Script",
    "SQL",
    "Section",
    "Markup",
    "Statement",
    "utils",
]
from .configuration import Configuration
from .connector import Connector, Connect
from .markup import Markup, Section
from .sql import SQL
from .statement import Statement

from .script import Script  # isort:skip
from .loader import Loader  # isort:skip
