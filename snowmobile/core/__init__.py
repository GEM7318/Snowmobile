"""
All modules housed in ``snowmobile.core`` to keep from cluttering intellisense
completion when interacting with the user-facing API.
"""
# isort: skip_file
from .exception_handler import ExceptionHandler
from .configuration import Configuration
from .connector import Connector
from .connector import Connector as Connect
from .section import Section
from .scope import Scope
from .tag import Tag
from .statement import Statement
from snowmobile.core import errors, schema, utils
from .column import Column
from .qa import Diff, Empty
from .snowframe import SnowFrame
from .sql import SQL
from .markup import Markup
from .script import Script
from .loader import Loader
from .paths import DDL_DEFAULT_PATH, DIR_MODULES, DIR_PKG_DATA, EXTENSIONS_DEFAULT_PATH


__all__ = [
    # core object model
    "Configuration",
    "Connector",
    "Connect",
    "Loader",
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
