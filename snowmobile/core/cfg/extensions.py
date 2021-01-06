"""
[external-sources] from **snowmobile.toml**.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import Field

from .base import Base


class Location(Base):
    """[external-sources]"""

    # fmt: off
    ddl: Path = Field(
        default_factory=Path, alias="ddl"
    )
    extensions: Path = Field(
        default_factory=Path, alias="snowmobile_ext"
    )
    sql_export_heading: Path = Field(
        default_factory=Path, alias="sql-export-heading"
    )
    # fmt: on
