"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from typing import Dict

from pydantic import Field

from .base import Base


class Put(Base):
    """Default 'put' statement arguments."""

    auto_compress: bool = Field(default_factory=bool, alias="auto_compress")


class Copy(Base):
    """Default 'copy into' statement arguments"""

    on_error: str = Field(default_factory=str, alias="on_error")


class Other(Base):
    """Default output-file options"""

    # fmt: off
    keep_local: bool = Field(
        default_factory=bool, alias="keep-local-file"
    )
    include_loaded_tmstmp: bool = Field(
        default_factory=bool, alias="include-loaded-timestamp"
    )
    # fmt: on


# noinspection PyUnresolvedReferences
class Loading(Base):
    """Default settings to use when loading data.

    Attributes:
        default-file-format (str):
            Name of file-format to use when loading data into the warehouse;
            default is ``snowmobile_default_csv``;
            # TODO: See more on file formats ______
            which will be created and
            dropped afterwards if an existing file format is not specified;
        include_index (bool):
            Include the index of a DataFrame when loading it into a table;
            default is ``False``.
        on_error (bool):
            Action to take if an error is encountered when loading data into
            the warehouse; default is ``continue``.
        keep_local (bool):
            Option to keep the local file exported when loading into a
            staging table; default is ``False``.
        include_loaded_tmstmp (bool):
            Include a **loaded_tmstmp** column when loading a DataFrame into
            the warehouse; default is ``True``.
        quote_char (str):
            Quote character to use for delimited files; default is double
            quotes (``"``).
        auto_compress (bool):
            Auto-compress file when loading data; default is ``True``..
        overwrite_pre_existing_stage (bool):
            Overwrite pre-existing staging table if data is being appended
            into an existing table/the staging table already exists; default is
            ``True``.

    """

    # fmt: off
    default_file_format: str = Field(
        default_factory=str, alias="default-file-format"
    )
    put: Put = Field(
        default_factory=Put, alias="put"
    )
    copy_into: Copy = Field(
        default_factory=Copy, alias="copy-into"
    )
    other: Other = Field(
        default_factory=Other, alias="other"
    )
    export_options: Dict[str, Dict] = Field(
        default_factory=dict, alias="export-options"
    )
    # fmt: on
