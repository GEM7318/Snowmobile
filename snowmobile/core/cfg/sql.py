"""[sql] (**snowmobile_ext.toml**)"""
from __future__ import annotations

import re

from typing import Dict, List

from pydantic import Field

from .base import Base


class SQL(Base):
    """[sql] (**snowmobile_ext.toml**)"""

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
        """Returns information schema table for object if other than making plural.

        i.e.:
            *   'table' --> 'tables'
            *   'schema' --> 'schemata'

        """
        obj = obj.strip("s")
        default = f"{obj}s"  # 'table' -> 'tables' / 'column' -> 'columns'
        return f"information_schema.{self.info_schema_exceptions.get(obj, default)}"

    def objects_within(self, first_line: str):
        """Searches the first line of sql for matches to named objects."""
        matched_terms = {
            i: re.findall(f"\\b{term}\\b", first_line)
            for i, term in enumerate(self.named_objects)
        }
        return {k: v[0] for k, v in matched_terms.items() if v}
