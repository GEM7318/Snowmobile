"""
``snowmobile`` lives in ``snowmobile.core`` to keep from cluttering
intellisense/autocomplete while interacting with the API.
"""
# isort: skip_file
from .base import Snowmobile
from .exception_handler import ExceptionHandler
from .configuration import Configuration
from .connector import Connector
from .connector import Connector as Connect
from .connector import Connector as connect
from .section import Section
from .scope import Scope
from .tag import Tag
from .statement import Statement
from snowmobile.core import errors, cfg, utils
from .column import Column
from .qa import Diff, Empty
from .snowframe import SnowFrame
from .sql import SQL
from .markup import Markup
from .script import Script
from .table import Table
from .paths import (
    # directories
    DIR_MODULES,
    DIR_PKG_DATA,
    # files
    DDL_DEFAULT_PATH,
    EXTENSIONS_DEFAULT_PATH,
    SQL_EXPORT_HEADING_DEFAULT_PATH,
)


__all__ = [
    # core object model
    "Snowmobile",
    "Configuration",
    "Connector", "Connect", "connect",
    "Table",
    "Script",
    "SQL",
    "Scope",
    "Section",
    "Markup",
    "Statement",
    "Diff",
    "Empty",
    "SnowFrame",
    "Column",
    "Tag",
    # parsed `snowmobile.toml` objects
    "cfg",
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
