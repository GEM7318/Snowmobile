"""
Flexible loading of data from a local DataFrame into a table.
"""
from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from pandas.io.sql import DatabaseError as pdDataBaseError
from snowflake.connector.errors import DatabaseError, ProgrammingError

from snowmobile.core import SQL, Connector, Script
from snowmobile.core.configuration import DDL_DEFAULT_PATH
from snowmobile.core.script import StatementNotFoundError

from .errors import (
    ColumnMismatchError,
    ExistingTableError,
    FileFormatNameError,
    LoadingInternalError,
)


# TODO: (rename) Loader -> Table
class Loader:

    def __init__(
        self,
        df: pd.DataFrame,
        table: str,
        sn: Connector,
        if_exists: Optional[str] = None,
        path_ddl: Optional[Path] = None,
        path_output: Optional[str, Path] = None,
        file_format: Optional[str] = None,
        incl_tmstmp: bool = True,
        tmstmp_col_nm: Optional[str] = None,
        reformat_cols: bool = True,
        validate_format: bool = True,
        upper_case_cols: bool = True,
        lower_case_table: Optional[bool] = False,
        keep_local: bool = False,
        on_error: Optional[str] = None,
    ):
        # sql generation and execution
        # ----------------------------
        self.sql: SQL = SQL(sn=sn, nm=table)

        # flow control
        # ------------
        self.msg: str = str()
        self.error: Any[
            LoadingInternalError,
            ExistingTableError,
            ColumnMismatchError,
            FileFormatNameError,
        ] = None
        self.requires_sql: bool = bool()

        # dataframe / table information
        # -----------------------------
        self.df = df.snf.upper() if upper_case_cols else df
        self.name: str = table.upper() if not lower_case_table else table
        self._exists: bool = bool()
        self._col_diff: Dict[int, bool] = dict()

        # argument specs + snowmobile.toml
        # --------------------------------
        self.path_ddl = path_ddl or DDL_DEFAULT_PATH
        self.path_output = path_output or Path.cwd() / f"{table}.csv"
        self.keep_local = keep_local or sn.cfg.loading.other.keep_local
        self.on_error = on_error or sn.cfg.loading.copy_into.on_error
        self.file_format = file_format or sn.cfg.loading.default_file_format
        self.if_exists = if_exists or sn.cfg.loading.default_if_exists

        # time tracking
        # -------------
        self._upload_validation_start: int = int()
        self._upload_validation_end: int = int()
        self._load_start: int = int()
        self._load_end: int = int()

        # file format validation
        # ----------------------
        if validate_format:
            format_exists_in_schema = self.file_format.lower() in [
                c.lower() for c in self.sql.show_file_formats().snf.to_list("name")
            ]
            if not format_exists_in_schema:  # read from source file otherwise
                assert self.path_ddl.exists(), f"{self.path_ddl} does not exist"
                ddl = Script(sn=self.sql.sn, path=self.path_ddl)
                st_name = f"create-file format~{self.file_format}"
                args = {  # only used if exception is thrown below
                    "nm": st_name,
                    "statements": list(ddl.contents(by_index=False)),
                }
                try:
                    ddl.run(st_name, results=False)
                except StatementNotFoundError(**args) as e:
                    raise FileFormatNameError(**args) from e

        # load timestamp
        # --------------
        if incl_tmstmp:
            col_nm = tmstmp_col_nm or "loaded_tmstmp"
            self.df.snf.add_tmstmp(
                col_nm=col_nm.upper() if upper_case_cols else col_nm.lower()
            )

        # column formatting
        # -----------------
        if reformat_cols:
            self.df.snf.reformat()

        # other
        # -----
        self.db_responses: Dict[str, str] = dict()
        self.loaded: bool = bool()

    @property
    def exists(self):
        """Indicates if the target table exists."""
        if not self._exists:
            self._exists = self.sql.exists()
        return self._exists

    @property
    def col_diff(self) -> Dict[int, bool]:
        """Returns diff detail of local DataFrame to in-warehouse table."""

        def fetch(idx: int, from_list: List) -> str:
            """Grab list item without throwing error if index exceeds length."""
            return str(from_list[idx]).lower() if idx <= (len(from_list) - 1) else None

        if self._col_diff:
            return self._col_diff
        if not self.exists:
            raise LoadingInternalError(
                nm="Table.col_diff()", msg=f"called while `table.exists={self.exists}`."
            )

        cols_t = self.sql.columns()
        cols_df = list(self.df.columns)

        self._col_diff = {
            i: fetch(i, cols_t) == fetch(i, cols_df)
            for i in range(max(len(cols_t), len(cols_df)))
        }
        return self._col_diff

    @property
    def cols_match(self) -> bool:
        """Indicates if columns match between DataFrame and table."""
        return all(self.col_diff.values())

    def load_statements(self, from_script: Path):
        """Generates exhaustive list of the statements to execute for a given
        instance of loading a DataFrame."""
        load_statements = self._load_sql
        if self.requires_sql:
            load_statements.insert(0, self._load_prep_sql(from_script=from_script))
        return load_statements

    def to_local(self, quote_all: bool = True):
        """Export to local file via configuration in ``snowmobile.toml``."""
        export_options = self.sql.sn.cfg.loading.export_options[self.file_format]
        if quote_all:
            export_options["quoting"] = csv.QUOTE_ALL
        self.df.to_csv(self.path_output, **export_options)

    @property
    def tm_load(self) -> int:
        """Seconds elapsed during loading."""
        return int(self._load_end - self._load_start)

    @property
    def tm_validate_load(self) -> int:
        """Seconds elapsed during validation."""
        return int(self._upload_validation_end - self._upload_validation_start)

    @property
    def tm_total(self):
        """Total seconds elapsed for load."""
        return self.tm_load + self.tm_validate_load

    def validate(self, if_exists: str) -> None:
        """Validates load based on current state through a variety of operations.

        Args:
            if_exists (str):
                Desired behavior if table already exists; intended to be passed
                in from :meth:`table.load()` by default.

        """
        self.error = None  # wipe prior validation results
        self._upload_validation_start = time.time()

        if not self.exists:  # no validation needed
            self.msg = f"{self.name} does not exist."
            self.requires_sql = "ddl"
            self._upload_validation_end = time.time()
            return

        self._col_diff = self.col_diff
        if if_exists == "fail":
            self.msg = (
                f"`{self.name}` already exists and if_exists='fail' was "
                f"provided; please provide 'replace', 'append', or "
                f"'truncate' to continue loading with a pre-existing table."
            )
            self.error = ExistingTableError(msg=self.msg)

        elif self.cols_match and if_exists == "append":
            self.msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )

        elif self.cols_match and if_exists == "replace":
            self.msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )
            self.requires_sql = "ddl"

        elif self.cols_match and if_exists == "truncate":
            self.msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )
            self.requires_sql = "truncate"

        elif not self.cols_match and if_exists != "replace":
            self.msg = (
                f"`{self.name}` columns do not equal those in the local "
                f"DataFrame and if_exists='{if_exists}' was specified.\nEither"
                f" provide if_exists='replace' to overwrite the existing table "
                f"or see `table.col_diff` to inspect the mismatched columns."
            )
            self.error = ColumnMismatchError(msg=self.msg)

        elif not self.cols_match:
            self.msg = (
                f"`{self.name}` exists with mismatched columns to local "
                f"DataFrame; recreating the table with new DDL as specified "
                f"by if_exists='{if_exists}'"
            )
            self.requires_sql = "ddl"

        else:
            self.msg = (
                f"Unknown combination of arguments passed to "
                f"``loadable.to_table()``."
            )
            self.error = LoadingInternalError(msg=self.msg)

        self._upload_validation_end = time.time()

    def load(
        self,
        if_exists: Optional[str] = None,
        verbose: bool = True,
        from_script: Path = None,
        validate: bool = True,
        **kwargs,
    ) -> Loader:

        if_exists = if_exists or self.if_exists
        if if_exists not in ("fail", "replace", "append", "truncate"):
            raise ValueError(
                f"Value passed to `if_exists` is not a valid argument;\n"
                f"Accepted values are: 'fail', 'replace', 'append', and 'truncate'"
            )

        # check for table existence; validate if so, all respecting `if_exists`
        if validate:
            self.validate(if_exists=if_exists)
            if self.error:
                raise self.error

        try:
            self._stdout_starting(verbose)
            self.to_local()  # export to local file
            load_statements = self.load_statements(  # includes DDL if self.exists=False
                from_script=from_script
            )
            self._load_start = time.time()
            for i, s in enumerate(load_statements, start=1):
                self.db_responses[s] = self.sql.sn.query(sql=s)  # store db responses
                self._stdout_progress(i, s, load_statements, if_exists, verbose)
            self.loaded = True

        except (ProgrammingError, pdDataBaseError, DatabaseError) as e:
            self.loaded = False
            raise e

        finally:
            self._load_end = time.time()
            self.sql.drop(nm=f"{self.name}_stage", obj="stage")  # drop stage
            if not self.keep_local:
                os.remove(str(self.path_output))
            self._stdout_time(verbose=(not kwargs.get("silence") and self.loaded))

        return self

    @property
    def _load_sql(self) -> List[str]:
        """Generates sql for create stage/put/copy statements."""
        # fmt: off
        return [
            self.sql.create_stage(
                nm_stage=f"{self.name}_stage",
                nm_format=self.file_format,
                run=False,
            ),
            self.sql.put_file_from_stage(
                path=self.path_output,
                nm_stage=f"{self.name}_stage",
                run=False,
            ),
            self.sql.copy_into_table_from_stage(
                nm=self.name,
                nm_stage=f"{self.name}_stage",
                run=False
            ),
        ]
        # fmt: on

    def _load_prep_sql(self, from_script: Path) -> str:
        """Generates table DDL or truncate statement where applicable."""
        if self.requires_sql == "ddl" and not from_script:
            return self.df.snf.ddl(table=self.name)
        elif self.requires_sql == "ddl":
            return Script(path=from_script, sn=self.sql.sn).s(_id=self.name).sql
        else:
            return self.sql.truncate(nm=self.name, run=False)

    def _stdout_starting(self, verbose: bool):
        """Starting message."""
        if verbose:
            schema = self.sql.sn.conn.schema.lower()
            print(f"Loading into '{schema}.{self.name}`..")

    @staticmethod
    def _stdout_progress(
        i: int, s: str, st: List, if_exists: str, verbose: bool
    ) -> None:
        """"Progress message for stdout, including only first line of DDL."""
        if verbose:
            if i == 1 and len(st) == 4 and if_exists != "truncate":
                s = s.split("\n")[0] + " .."

            print(f"({i} of {len(st)})\n\t{s}")

    def _stdout_time(self, verbose: bool) -> None:
        """Time summary message for stdout."""
        if verbose:
            print(f"..completed: {self.df.shape[0]} rows in {self.tm_total} seconds")

    def __str__(self) -> str:
        return f"snowmobile.Loader(table='{self.name}')"

    def __repr__(self) -> str:
        return f"snowmobile.Loader(table='{self.name}')"
