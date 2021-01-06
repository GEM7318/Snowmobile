"""
[loading] section from **snowmobile.toml**, including subsections.
"""
from __future__ import annotations

from typing import Dict

from pydantic import Field

from .base import Base


class Put(Base):
    """[loading.put]"""

    auto_compress: bool = Field(default_factory=bool, alias="auto_compress")


class Copy(Base):
    """[loading.copy]"""

    on_error: str = Field(default_factory=str, alias="on_error")


# noinspection PyUnresolvedReferences
class Loading(Base):
    """[loading]

    Default settings to use when loading data

    Attributes:
        default-file-format (str):
            Name of file-format to use when loading data into the warehouse;
            default is ``snowmobile_default_csv``;
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
    defaults: Dict = Field(
        default_factory=dict, alias="default-table-kwargs"
    )
    put: Put = Field(
        default_factory=Put, alias="put"
    )
    copy_into: Copy = Field(
        default_factory=Copy, alias="copy-into"
    )
    export_options: Dict[str, Dict] = Field(
        default_factory=dict, alias="export-options"
    )
    # fmt: on

    @property
    def configured_args(self) -> Dict:
        """Placeholder for configuration arguments of derived classes."""
        return self.defaults
