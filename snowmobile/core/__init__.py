"""
All modules housed in ``snowmobile.core`` to keep from cluttering intellisense
completion when interacting with the user-facing API.
"""
from .exception_handler import ExceptionHandler  # isort: skip
from snowmobile.core import errors, schema, utils
from .configuration import Configuration
from .connector import Connector
from .connector import Connector as Connect
from .section import Section
from .scope import Scope
from .snowframe import SnowFrame
from .column import Column
from .tag import Tag
from .sql import SQL
from .statement import Statement
from .qa import Empty, Diff
from .paths import (
    DIR_MODULES, DIR_PKG_DATA, EXTENSIONS_DEFAULT_PATH, DDL_DEFAULT_PATH
)

from .markup import Markup  # isort: skip
from .script import Script  # isort:skip
from .loader import Loader  # isort:skip


__all__ = [
    # core object model
    "Configuration",
    "Connector",
    "Connect",
    "Loader",
    "Script",
    "SQL",
    "Section",
    "Scope",
    "Markup",
    "Statement",
    "Diff",
    "Empty",
    "SnowFrame",
    "Column",
    "Tag",

    # parsed `snowmobile.toml` objects
    "schema",

    # error/exception handling
    "ExceptionHandler",
    "errors",

    # file paths
    "DIR_PKG_DATA",
    "DDL_DEFAULT_PATH",
    "EXTENSIONS_DEFAULT_PATH",

    # other
    "utils",
]
