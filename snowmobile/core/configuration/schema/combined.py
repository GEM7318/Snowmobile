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
from .script import Script, Type


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


class Snowmobile(Base):
    """Full configuration object.

    Represents the parsed **snowmobile.toml** file.

    """

    # fmt: off
    connection: Connection = Field(
        default_factory=Connection, alias='connection'
    )
    loading: Loading = Field(
        default_factory=Loading, alias="loading-defaults"
    )
    script: Script = Field(
        default_factory=Script, alias='script'
    )
    sql: SQL = Field(
        default_factory=SQL, alias="sql"
    )
    ext_locations: Location = Field(
        default_factory=Location, alias='external-file-locations'
    )
    # fmt: on

    def __init__(self, **data):

        super().__init__(**data)

        with open(self.ext_locations.backend, "r") as r:
            backend = toml.load(r)

        self.script.types = self.script.types.from_dict(backend["tag-to-type-xref"])
        self.sql.from_dict(backend["sql"])

    # TODO: Stick somewhere that makes sense
    def sqlparse_stream(self, stream: str) -> sqlparse.sql.Statement:
        """Parses source sql into individual statements."""
        for s in sqlparse.parsestream(stream=stream):
            if self.script.is_valid_sql(s=s):
                yield s
