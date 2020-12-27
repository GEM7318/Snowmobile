"""
A wrapper library around the snowflake-connector-python for streamlined
interaction with the Snowflake database.
"""
# isort: skip_file
# fmt: off
__version__ = "0.1.14"
__author__ = "Grant Murray"
__application__ = "snowmobile"

__all__ = [
    # meta
    "__version__",
    "__author__",
    "__application__",

    # API
    "Connector",
    "Connect",
    "SQL",
    "Loader",
    "Configuration",
    "Script",
    "Statement",
]

from .core import (
    SQL,
    Configuration,
    Connect,
    Connector,
    Loader,
    Script,
    Section,
    Statement,
    utils,
)
