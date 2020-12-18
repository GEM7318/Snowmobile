"""
``snowmobile.Connect`` class; bundles together configuration object and
SnowflakeConnection for query/statement execution.
"""
from __future__ import annotations
from pathlib import Path
from typing import Union, ContextManager
from contextlib import contextmanager

import pandas as pd
from pandas.io.sql import DatabaseError

from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeConnection, SnowflakeCursor
from snowflake.connector.errors import ProgrammingError

import snowmobile.core.sql as sql
from snowmobile.core.configuration import Configuration
from snowmobile.core.df_ext import Frame


class Connector:
    """Primary Connection and Query Execution Class.

    Attributes:

        cfg (:class:`snowmobile.core.configuration.Configuration`):
            :class:`snowmobile.core.configuration.Configuration` object which
            includes attributes for all values within the **snowmobile.toml**.

    """

    def __init__(
        self,
        creds: str = None,
        config_file_nm: str = None,
        from_config: Union[str, Path] = None,
        ensure_alive: bool = True,
        delay: bool = False,
        mode: str = None,
        **kwargs,
    ):
        """

        Args:
            config_file_nm (str):
                Name of configuration file; defaults to `snowmobile.toml`.
            creds (str):
                Name of the set of credentials to authenticate with;
                defaults to what is specified in `default` within the
                configuration file or uses the first set of credentials in
                the file if neither is specified.
            from_config (pathlib.Path):
                Optionally specify a full path to the configuration file;
                primarily included for usage within containers/deployment
                with specific file-system configurations.

        """
        self._error: bool = bool()

        self.cfg: Configuration = Configuration(
            creds=creds,
            config_file_nm=config_file_nm,
            from_config=from_config
        )
        self.ensure_alive = ensure_alive
        # self.delayed = delay
        self.conn: SnowflakeConnection = None
        self.sql: sql.SQL = sql.SQL(sn=self)
        self.mode = mode or 'e'
        if not delay:
            self.connect(**kwargs)

    # DOCSTRING
    def connect(self, **kwargs) -> Connector:
        """Creates new connection to Snowflake with the same set of credentials.
            kwargs:
                Optional keyword arguments to pass to
                snowflake.connector.connect(); arguments passed here will
                over-ride ``connection.default-settings`` specified in
                ``snowmobile.toml``.
        """
        try:
            self.conn = connect(
                **{
                    **self.cfg.connection.current.credentials,  # credentials
                    **self.cfg.connection.defaults,             # defaults
                    **kwargs                                    # over-rides/additional
                },
            )
            # self.delayed = False
            self.sql = sql.SQL(sn=self)

            print(str(self))
            return self

        except ProgrammingError as e:
            raise ProgrammingError(e)

    def disconnect(self) -> Connector:
        """Disconnect from connection with which Connector() was instantiated."""
        self.conn.close()
        # self.delayed = True
        self.conn = None
        return self

    @property
    def alive(self) -> bool:
        """Check if the connection is still alive."""
        if not isinstance(self.conn, SnowflakeConnection):
            return False
        return not self.cursor.is_closed()

    @property
    def cursor(self) -> Union[SnowflakeCursor, None]:
        """:class:`SnowflakeCursor` accessor off :class:`snowmobile.Connect`."""
        if not isinstance(self.conn, SnowflakeConnection):
            self.connect()
        return self.conn.cursor()

    def ex(self, sql: str, **kwargs) -> SnowflakeCursor:
        """Executes a command via :class:`SnowflakeCursor`.

        Args:
            sql (str):
                ``sql`` command as a string.
            **kwargs:
                Optional keyword arguments for :meth:`SnowflakeCursor.execute()`.

        Returns (SnowflakeCursor):
            :class:`SnowflakeCursor` object that executed the command.

        """
        try:
            return self.cursor.execute(command=sql, **kwargs)
        except ProgrammingError as e:
            self._error = e
            raise ProgrammingError(f"ProgrammingError: {e}")

    def query(
        self, sql: str, results: bool = True, lower: bool = True,
    ) -> Union[pd.DataFrame, SnowflakeCursor]:
        """Executes a command and returns results as a :class:`DataFrame`.

        Args:
            sql (str):
                Raw SQL to execute.
            results (bool):
                Boolean value indicating whether or not to return results.
            lower (bool):
                Boolean value indicating whether or not to return results
                with columns lower-cased.

        Returns (Union[pd.DataFrame, SnowflakeCursor]):
            Results from ``sql`` as a :class:`DataFrame` by default or the
            :class:`SnowflakeCursor` object if `Results=False`.

        """
        if not results:
            return self.ex(sql=sql)

        try:
            self._connect()
            df = pd.read_sql(sql, con=self.conn)
            return df.snowmobile.lower_cols() if lower else df
        except DatabaseError as e:
            self._error = e
            raise e

    def _connect(self):
        """Connects to db if not connected and a connection is implicitly invoked."""
        if not self.alive and self.ensure_alive:
            self.connect()
        return self

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __str__(self) -> str:
        return f"snowmobile.Connect(creds='{self.cfg.connection.creds}')"

    def __repr__(self) -> str:
        return f"snowmobile.Connect(creds='{self.cfg.connection.creds}')"
