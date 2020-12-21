"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import sqlparse
import toml
from pydantic import Field

from .base import Base
from .connection import Connection
from .loading import Loading
from .script import Script


class Location(Base):
    # fmt: off
    ddl: Path = Field(
        default_factory=Path, alias="ddl"
    )
    backend: Path = Field(
        default_factory=Path, alias="backend-ext"
    )
    # fmt: on


class SQL(Base):
    # fmt: off
    generic_anchors: Dict = Field(
        default_factory=dict, alias="generic-anchors"
    )
    kw_exceptions: Dict = Field(
        default_factory=dict, alias="keyword-exceptions"
    )
    named_objects: List = Field(
        default_factory=list, alias="named-objects"
    )
    # fmt: on


class Snowmobile:
    """Full configuration object.

    Represents the parsed **snowmobile.toml** file.

    """

    def __init__(
        self, **kwargs,
    ):
        # fmt: off
        self.connection = Connection(**kwargs.get('connection', {}))
        self.loading = Loading(**kwargs.get('loading-defaults', {}))
        self.script = Script(**kwargs.get('script', {}))
        self.sql = SQL(**kwargs.get('sql', {}))
        self.ext_locations = Location(**kwargs.get('external-file-locations', {}))
        # fmt: on

        with open(self.ext_locations.backend, "r") as r:
            backend = toml.load(r)

        self.script.types = self.script.types.from_dict(backend["tag-to-type-xref"])
        self.sql.from_dict(backend["sql"])
