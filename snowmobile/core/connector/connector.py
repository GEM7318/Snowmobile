"""
``snowmobile.Connect`` class; bundles together configuration object and
SnowflakeConnection for query/statement execution.
"""
from __future__ import annotations
from pathlib import Path
from typing import Union

import pandas as pd
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
        self.cfg: Configuration = Configuration(
            config_file_nm=config_file_nm, creds=creds, from_config=from_config
        )
        self.ensure_alive = ensure_alive
        self._delayed = delay
        self.conn: SnowflakeConnection = None
        self.sql: sql.SQL = sql.SQL(sn=self)
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
                    **self.cfg.connection.current.credentials,
                    **self.cfg.connection.defaults,
                    **kwargs
                },
            )

            self._delayed = False
            self.sql = sql.SQL(sn=self)

            print(self)
            return self

        except ProgrammingError as e:
            raise ProgrammingError(e)

    def disconnect(self) -> Connector:
        """Disconnect from connection with which Connector() was instantiated."""
        self.conn.close()
        self._delayed = True
        return self

    @property
    def alive(self) -> bool:
        """Check if the connection is still alive."""
        return False if self._delayed else not self.cursor.is_closed()

    @property
    def cursor(self) -> SnowflakeCursor:
        """:class:`SnowflakeCursor` accessor off :class:`snowmobile.Connect`."""
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
        return self.cursor.execute(command=sql, **kwargs)

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
        if self._delayed or (self.ensure_alive and not self.alive):
            self.connect()
        try:
            if not results:
                return self.ex(sql)
            df = pd.read_sql(sql, con=self.conn)
            return df.snowmobile.lower_cols() if lower else df

        except ProgrammingError as e:
            raise ProgrammingError(f"ProgrammingError: {e}")

    def __str__(self) -> str:
        return f"snowmobile.Connect(creds='{self.cfg.connection.creds}')"

    def __repr__(self) -> str:
        return f"snowmobile.Connect(creds='{self.cfg.connection.creds}')"
