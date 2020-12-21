"""
Module handles flexible loading of data from a local DataFrame into a table.
"""
from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd

from snowmobile.core import (
    Connector,
    Script,
    SQL,
)
from snowmobile.core.configuration import DDL_DEFAULT_PATH


class Loader:
    def __init__(
        self,
        df: pd.DataFrame,
        table: str,
        sn: Connector,
        keep_local: bool = False,
        output_location: Union[str, Path] = None,
        on_error: str = None,
        file_format: str = None,
        add_tmstmp: bool = True,
        tmstmp_col_nm: str = None,
        reformat_cols: bool = True,
        upper_case_cols: bool = True,
        format_ddl_src: Path = None,
        skip_format_validation: bool = False,
    ):
        self._continue_load: bool = bool()
        self._msg: str = str()
        self._validated: bool = bool()
        self._requires_sql: bool = bool()
        self._raise_error: bool = bool()
        self._exists: bool = bool()

        self.df = df.snowmobile.upper_cols() if upper_case_cols else df
        self.name: str = table
        self.sn: Connector = sn
        self.sql: SQL = SQL(sn=sn, nm=table)
        self.format_ddl_src = format_ddl_src or DDL_DEFAULT_PATH

        self.keep_local = keep_local or sn.cfg.loading.other.keep_local
        self.output_location = output_location or Path.cwd() / f"{table}.csv"
        self.on_error = on_error or sn.cfg.loading.copy_into.on_error
        self.file_format = file_format or sn.cfg.loading.default_file_format

        if add_tmstmp:
            col_nm = tmstmp_col_nm or "loaded_tmstmp"
            self.df.snowmobile.add_tmstmp(
                col_nm=col_nm.upper() if upper_case_cols else col_nm.lower()
            )
        if reformat_cols:
            self.df.snowmobile.reformat_cols()

        self.db_responses: Dict[str, str] = dict()
        self.start_time: int = int()
        self.end_time: int = int()
        self.loaded: bool = bool()
        self.col_diff: dict = dict()
        self.cols_match: bool = False

        if not skip_format_validation:
            self._file_format_incl_schema = (
                f"{self.sn.conn.schema}.{self.file_format}".lower()
            )
            self.queried_format_ddl = self._get_format_ddl()
            self._file_format_exists_in_current_schema = (
                self._file_format_incl_schema in self.queried_format_ddl
            )
            self._file_format_exists_in_other_schema = self.file_format.lower() in {
                k.split(".")[1].lower() for k in self.queried_format_ddl.keys()
            }
            self._validate_provided_file_format()

    def _get_format_ddl(self):
        file_formats = {}
        for _, dtl in self.sql.show_file_formats().to_dict(orient="index").items():
            args = {
                "nm": dtl["name"],
                "obj": "file_format",
            }
            if args["obj"].lower() == self.file_format.lower():
                format_nm_incl_schema = f"{dtl['schema_name']}.{dtl['name']}".lower()
                file_formats[format_nm_incl_schema] = self.sql.ddl(**args)
        return file_formats

    def _validate_provided_file_format(self):
        # fmt: off
        if self._file_format_exists_in_current_schema:
            pass

        elif self.file_format == self.sn.cfg.loading.default_file_format:

            ddl_sql = Script(sn=self.sn, path=self.format_ddl_src)
            expected_statement_nm = f"create-file format~{self.file_format}"
            try:
                ddl_sql.statement(_id=expected_statement_nm).run()
            except ValueError:
                raise ValueError(
                    f"{expected_statement_nm} not found in {self.format_ddl_src.as_posix()}."
                    f" Either provide a different value for `format_ddl_src` "
                    f"or specify a different `file_format`."
                )

        elif self._file_format_exists_in_other_schema:
            raise Exception(
                f"{self.file_format} detected in other schema. Execute one of "
                f"the ddl statements in ``loader.queried_format_ddl`` to create "
                f"format in the current schema."
            )

        else:
            raise Exception(
                f"File format '{self.file_format}' is not detected in any "
                f"schemas. Please create file format in {self.sn.conn.schema} "
                f"before re-attempting load or specify a different `file_format`."
            )
        # fmt: on

    def _compare_fields(self) -> dict:
        def safe_get(get_from: List, idx_to_get: int):
            """Grabs item from a list without an error if index exceeds length
            of the list"""
            max_idx = len(get_from) - 1
            return get_from[idx_to_get] if idx_to_get <= max_idx else None

        assert (
            self._exists
        ), "Loader._compare_fields() called prior to verifying table exists."
        # fmt: off
        match_dtl = {}
        table_cols = self.sql.columns(nm=self.name)
        df_cols = list(self.df.columns)
        safe_idx = max(len(table_cols), len(df_cols))
        for i in range(safe_idx):

            table_col = safe_get(table_cols, i)
            df_col = safe_get(df_cols, i)

            match_true = table_col == df_col

            match_sans_case = (
                str(table_col).lower() == str(df_col).lower()
                if table_col and df_col else False
            )

            dtl = {
                'warehouse_col': table_col,
                'df_col': df_col,
                'matches_all': match_true,
                'matches_values': match_sans_case
            }

            match_dtl[i] = dtl
        # fmt: on
        return match_dtl

    @property
    def load_sql(self) -> List[str]:
        """Generates sql for stage-creation/put/copy statements."""
        # fmt: off
        return [
            self.sql.create_stage(
                nm_stage=f"{self.name}_stage",
                nm_format=self.file_format,
                run=False,
            ),
            self.sql.put_file_from_stage(
                path=self.output_location,
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
        if self._requires_sql == "ddl" and not from_script:
            return self.df.snowmobile.ddl(table=self.name)
        elif self._requires_sql == "ddl":
            return Script(path=from_script, sn=self.sn).statement(_id=self.name).sql
        else:
            return self.sql.truncate(nm=self.name, run=False)

    def load_statements(self, from_script: Path):
        """Generates exhaustive list of the statements to execute for a given
        instance of loading a DataFrame."""
        load_statements = self.load_sql
        if self._requires_sql:
            load_statements.insert(0, self._load_prep_sql(from_script=from_script))
        return load_statements

    def to_local(self, quote_all: bool = True):
        """Utility to export DataFrame to a .csv without cluttering :meth:`load()`."""
        export_options = \
            self.sn.cfg.loading.export_options[self.file_format]
        export_options['path_or_buf'] = self.output_location
        if quote_all:
            export_options['quoting'] = csv.QUOTE_ALL
        self.df.to_csv(**export_options)

    def diff_cols(self, table_exists: bool = True) -> None:
        self.col_diff = self._compare_fields() if table_exists else dict()
        self.cols_match = (
            all(d["matches_values"] for d in self.col_diff.values())
            if table_exists
            else False
        )

    # TODO: wtf is this actually doing
    @staticmethod
    def _format_db_response(df: pd.DataFrame):
        responses = [
            f"{' '.join(col.title().split('_'))}: {df.iat[0, i1]}"
            for i1, col in enumerate(list(df.columns))
        ]
        return "\n\t".join(responses)

    @property
    def db_response(self):
        compiled = [
            f"\n({i}) `{k}`\n{v}"
            for i, (k, v) in enumerate(self.db_responses.items(), start=1)
        ]
        return "\n".join(compiled)

    @property
    def load_time(self) -> int:
        return int(self.end_time - self.start_time)

    # noinspection PyUnboundLocalVariable
    def validate(self, if_exists: str, validate: bool = True) -> None:

        if validate:
            self._exists = self.sql.exists(nm=self.name)
            self.diff_cols(table_exists=self._exists)
        else:
            (
                self._continue_load,
                self._requires_sql,
                self._raise_error,
                self._msg,
                self._validated,
            ) = (True, str(), False, str(), False)
            return

        if not self._exists:
            msg = f"{self.name} does not exist."
            continue_load, requires_sql, raise_error = True, "ddl", False

        elif if_exists == "fail":
            msg = (
                f"`{self.name}` already exists and if_exists='fail' was "
                f"provided; please provide 'replace', 'append', or 'truncate' "
                f"to continue loading with a pre-existing table."
            )
            continue_load, requires_sql, raise_error = False, "", True

        elif self.cols_match and if_exists == "append":
            msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )
            continue_load, requires_sql, raise_error = True, "", False

        elif self.cols_match and if_exists == "replace":
            msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )
            continue_load, requires_sql, raise_error = True, "ddl", False

        elif self.cols_match and if_exists == "truncate":
            msg = (
                f"`{self.name}` exists with matching columns to local "
                f"DataFrame; if_exists='{if_exists}'"
            )
            continue_load, requires_sql, raise_error = True, "truncate", False

        elif not self.cols_match and if_exists != "replace":
            msg = (
                f"`{self.name}` exists with mismatched columns to local "
                f"DataFrame and if_exists='{if_exists}' was specified. "
                f"Either provide a different value for `if_exists` or see "
                f"``loadable.col_diff`` to inspect the mismatched columns."
            )
            continue_load, requires_sql, raise_error = False, "", True

        elif not self.cols_match:
            msg = (
                f"`{self.name}` exists with mismatched columns to local "
                f"DataFrame; recreating the table with new DDL as specified "
                f"by if_exists='{if_exists}'"
            )
            continue_load, requires_sql, raise_error = True, "ddl", False

        else:
            msg = (
                f"Unknown combination of arguments passed to "
                f"``loadable.to_table()``."
            )
            continue_load, requires_sql, raise_error = False, "", True

        (
            self._continue_load,
            self._requires_sql,
            self._raise_error,
            self._msg,
            self._validated,
        ) = (continue_load, requires_sql, raise_error, msg, True)

    def load(
        self,
        if_exists: str = None,
        verbose: bool = True,
        from_script: Path = None,
        validate: bool = True,
    ) -> Loader:

        if_exists = if_exists or "append"

        # validate value provided for `if_exists`
        if if_exists not in ("fail", "replace", "append", "truncate"):
            raise ValueError(
                f"Value passed to `if_exists` is not a valid argument;\n"
                f"Accepted values are: 'fail', 'replace', 'append', 'truncate'"
            )

        # check for table existence; validate if so, all respecting `if_exists`
        self.validate(if_exists=if_exists, validate=validate)
        assert not self._raise_error and self._continue_load, self._msg

        try:
            # export local file; generate statements to execute
            self.to_local()
            load_statements = self.load_statements(from_script=from_script)
            if verbose:
                print(f"Loading into '{self.sn.conn.schema.lower()}.{self.name}`..")

            # set start time; execute statements; save responses from db
            self.start_time = time.time()
            for i, s in enumerate(load_statements, start=1):
                response = self._format_db_response(self.sn.query(sql=s))
                self.db_responses[s] = response
                if verbose:
                    print(f"<{i} of {len(load_statements)}>\n\t`{s}`")

            self.loaded = True

        # raise exception and print db response if statements cause an error
        except Exception as e:
            self.loaded = False
            raise e

        finally:
            # set end-time; drop stage; remove local file if specified
            self.end_time = time.time()

            self.sql.drop(nm=f"{self.name}_stage", obj="stage")

            if not self.keep_local:
                os.remove(str(self.output_location))

            if verbose and self.loaded:
                print(f"Load completed in {self.load_time} seconds.")

        return self

    def __str__(self) -> str:
        return f"snowmobile.Loader(table='{self.name}')"

    def __repr__(self) -> str:
        return f"snowmobile.Loader(table='{self.name}')"
