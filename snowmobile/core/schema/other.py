"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from pydantic import Field

from .base import Base


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
    info_schema_exceptions: Dict[str, str] = Field(
        default_factory=dict, alias="information-schema-exceptions"
    )
    # fmt: on

    def info_schema_loc(self, obj: str) -> str:
        """Returns information schema location from an object."""
        obj = obj.strip("s")
        default = f"{obj}s"  # 'table' -> 'tables'/'column' -> 'columns'
        return f"information_schema.{self.info_schema_exceptions.get(obj, default)}"
