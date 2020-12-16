"""
Majority of library contained within subsequent ``snowmobile.core`` modules;
buried in ``core`` to keep from cluttering intellisense/auto-complete
recommendations when interacting with ``snowmobile`` objects.
"""
__all__ = [
    "Configuration",
    "Connector",
    "Loader",
    "Script",
    "SQL",
    "Section",
    "Doc",
    "Statement",
    "utils",
]
from .configuration import Configuration
from .connector import Connector
from .document import Doc, Section
from .sql import SQL
from .statement import Statement

from .script import Script  # isort:skip
from .loader import Loader  # isort:skip
