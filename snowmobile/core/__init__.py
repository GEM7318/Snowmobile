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
    "Diff",
    "Empty",
    "SnowFrame",
    "utils",
    "errors",
    "ExceptionHandler"
]
from snowmobile.core import errors

from .configuration import Configuration
from .connector import Connector
from .connector import Connector as Connect
from .markup import Markup, Section
from .snowframe import SnowFrame
from .sql import SQL
from .statement import Statement
from .qa import Empty, Diff
from .exception_handler import ExceptionHandler

from .script import Script  # isort:skip
from .loader import Loader  # isort:skip


# ====================================
# -- Static path variables accessed --
# -- across `snowmobile.core`.      --
# ====================================

# from pathlib import Path
#
# # -- directories
# _DIR_MODULES = Path(__file__).absolute().parent
# _DIR_PKG_DATA = _DIR_MODULES / 'pkg_data'
#
# # -- files
# _PATH_EXTENSIONS_DEFAULT = _DIR_PKG_DATA / 'snowmobile_backend.toml'
# _PATH_DDL_DEFAULT = _DIR_PKG_DATA / 'DDL.sql'
