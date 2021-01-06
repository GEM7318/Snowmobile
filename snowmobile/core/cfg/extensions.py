"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from pathlib import Path

from pydantic import Field

from .base import Base


class Location(Base):
    # fmt: off
    ddl: Path = Field(
        default_factory=Path, alias="ddl"
    )
    backend: Path = Field(
        default_factory=Path, alias="extension"
    )
    # fmt: on
