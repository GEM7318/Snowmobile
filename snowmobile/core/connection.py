"""
:class:`snowmobile.connection` is the core of ``snowmobile``'s object model and a given
instance is often shared across multiple objects at once.

It is the primary method of executing statements against the warehouse and
it stores the fully parsed & validated ``snowmobile.toml`` file it was
instantiated with as its :attr:`snowmobile.cfg` attribute.

Within ``snowmobile``'s code and documentation, it is referred to as ``sn``
for brevity.

"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd
from pandas.io.sql import DatabaseError as pdDataBaseError
from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeCursor
from snowflake.connector import (
    DictCursor,
    SnowflakeConnection,
    DatabaseError,
    ProgrammingError,
)

from snowmobile.core import sql
from snowmobile.core import ExceptionHandler
from snowmobile.core.snowframe import SnowFrame

from . import Configuration
from . import Generic


class Snowmobile(Generic):
    """Primary method of statement execution and accessor to parsed snowmobile.toml.

    Args:

        creds (Optional[str]):
            Alias for the set of credentials to authenticate with; default
            behavior will fall back to the ``connection.default-creds``
            specified in `snowmobile.toml`, `or the first set of credentials
            stored if this configuration option is left blank`.
        delay (bool):
            Optionally delay establishing a connection when the object is
            instantiated, enabling access to the configuration object model
            through the :attr:`Connection.cfg` attribute; defaults to `False`.
        ensure_alive (bool):
            Establish a new connection if a method requiring a connection
            against the database is called while :attr:`alive` is `False`;
            defaults to `True`.
        config_file_nm (Optional[str]):
            Name of configuration file to use; defaults to `snowmobile.toml`.
        from_config (Optional[str, Path]):
            A full path to a specific configuration file to use; bypasses any
            checks for a cached file location and can be useful for container-based
            processes with restricted access to the local file system.
        **connect_kwargs:
            Additional arguments to provide to :meth:`snowflake.connector.connect()`;
            arguments provided here will over-ride connection arguments specified
            in `snowmobile.toml`, including:
                *   Connection parameters in `connection.default-arguments`
                *   Credentials parameters associated with a given alias
                *   Connection parameters associated with a given alias


    Attributes:

        cfg (Configuration`):
            :class:`snowmobile.Configuration` object, which represents a fully
            parsed/validated `snowmobile.toml` file.
        con (SnowflakeConnection):
            :class:`SnowflakeConnection` object; this attribute is populated
            when a connection is established and can be `None` if the
            :class:`Connection` object was instantiated with `delay=True`.
        sql (SQL):
            A :class:`snowmobile.SQL` object with the current connection
            embedded; stores command sql commands as utility methods and is
            heavily leveraged in `snowmobile`'s internals.
        ensure_alive (bool):
            Establish a new connection if a method requiring a connection
            against the database is called while :attr:`alive` is `False`;
            defaults to `True`.
        e (ExceptionHandler):
            A :class:`snowmobile.ExceptionHandler` object for orchestrating
            exceptions across objects; kept as a public attribute on the class
            as examining its contents can be helpful in debugging database errors
            during development.

    """

    def __init__(
        self,
        creds: Optional[str] = None,
        delay: bool = False,
        ensure_alive: bool = True,
        config_file_nm: Optional[str] = None,
        from_config: Optional[str, Path] = None,
        **connect_kwargs,
    ):
        super().__init__()

        self.cfg: Configuration = Configuration(
            creds=creds, config_file_nm=config_file_nm, from_config=from_config
        )
        self.ensure_alive = ensure_alive
        self.con: Optional[SnowflakeConnection] = None
        self.sql: sql.SQL = sql.SQL(sn=self)
        self.e: ExceptionHandler = ExceptionHandler(within=self).set(ctx_id=-1)

        if not delay:
            self.connect(**connect_kwargs)

    def connect(self, **kwargs) -> Snowmobile:
        """Establishes connection to Snowflake.

        Re-implements :func:`snowflake.connector.connect()` with connection
        arguments sourced from snowmobile's object model, specifically:
            *   Credentials from ``snowmobile.toml``.
            *   Default connection arguments from ``snowmobile.toml``.
            *   Optional keyword arguments either passed to
                :class:`snowmobile.connect` or directly to this method.

            kwargs:
                Optional keyword arguments to pass to
                snowflake.connector.connect(); arguments passed here will
                over-ride ``connection.default-arguments`` specified in
                ``snowmobile.toml``.

        """
        try:
            self.con = connect(
                **{
                    **self.cfg.connection.connect_kwargs,  # snowmobile.toml
                    **kwargs,  # any kwarg over-rides
                }
            )
            self.sql = sql.SQL(sn=self)
            print(f"..connected: {str(self)}")
            return self

        except DatabaseError as e:
            raise e

    def disconnect(self) -> Snowmobile:
        """Disconnect from connection with which Connection() was instantiated."""
        self.con.close()
        self.con = None
        return self

    @property
    def alive(self) -> bool:
        """Check if the connection is alive."""
        if not isinstance(self.con, SnowflakeConnection):
            return False
        return not self.cursor.is_closed()

    @property
    def cursor(self) -> SnowflakeCursor:
        """:class:`SnowflakeCursor` accessor."""
        if not isinstance(self.con, SnowflakeConnection) and self.ensure_alive:
            self.connect()
        return self.con.cursor()

    # noinspection PydanticTypeChecker,PyTypeChecker
    @property
    def dictcursor(self) -> DictCursor:
        """:class:`DictCursor` accessor."""
        # TODO: check type hint in source code for SnowflakeConnection.cursor()
        #  method to figure out why intellisense is yelling about this;
        #  shouldn't it be Union[SnowflakeCursor, DictCursor]?
        if not isinstance(self.con, SnowflakeConnection) and self.ensure_alive:
            self.connect()
        return self.con.cursor(cursor_class=DictCursor)

    def ex(self, sql: str, on_error: Optional[str] = None, **kwargs) -> SnowflakeCursor:
        """Executes a command via :class:`SnowflakeCursor`.

        Args:
            sql (str):
                ``sql`` command as a string.
            on_error (str):
                String value to impose a specific behavior if an error occurs
                during the execution of ``sql``.
            **kwargs:
                Optional keyword arguments for :meth:`SnowflakeCursor.execute()`.

        Returns (SnowflakeCursor):
            :class:`SnowflakeCursor` object that executed the command.

        """
        try:
            return self.cursor.execute(command=sql, **kwargs)
        except ProgrammingError as e:
            e.to_raise = on_error != 'c'
            self.e.collect(e=e)
            if e.to_raise:
                raise e

    def exd(self, sql: str, on_error: Optional[str] = None, **kwargs) -> DictCursor:
        """Executes a command via :class:`DictCursor`.

        Args:
            sql (str):
                ``sql`` command as a string.
            on_error (str):
                String value to impose a specific behavior if an error occurs
                during the execution of ``sql``.
            **kwargs:
                Optional keyword arguments for :meth:`SnowflakeCursor.execute()`.

        Returns (DictCursor):
            :class:`DictCursor` object that executed the command.

        """
        try:
            return self.dictcursor.execute(command=sql, **kwargs)
        except ProgrammingError as e:
            e.to_raise = on_error != 'c'
            self.e.collect(e=e)
            if e.to_raise:
                raise e

    def query(
        self,
        sql: str,
        as_df: bool = True,
        lower: bool = True,
        on_error: Optional[str] = None,
    ) -> Union[pd.DataFrame, SnowflakeCursor]:
        """Execute a query and return results.

         Default behavior of `results=True` will return results as a
         :class:`pandas.DataFrame`, otherwise will execute the sql provided
         with a :class:`SnowflakeCursor` and return the cursor object.

        Args:
            sql (str):
                Raw SQL to execute.
            as_df (bool):
                Boolean value indicating whether or not to return results.
            lower (bool):
                Boolean value indicating whether or not to return results
                with columns lower-cased.
            on_error (str):
                String value to impose a specific behavior if an error occurs
                during the execution of ``sql``.

        Returns (Union[pd.DataFrame, SnowflakeCursor]):
            Results from ``sql`` as a :class:`DataFrame` by default or the
            :class:`SnowflakeCursor` object if `results=False`.

        """
        if not as_df:
            return self.ex(sql=sql)

        try:
            if not self.alive and self.ensure_alive:
                self.connect()

            df = pd.read_sql(sql, con=self.con)
            return df.snf.lower() if lower else df

        except (pdDataBaseError, DatabaseError) as e:
            e.to_raise = on_error != 'c'
            self.e.collect(e=e)
            if e.to_raise:
                raise e

    def __str__(self) -> str:
        return f"snowmobile.Snowmobile(creds='{self.cfg.connection.creds}')"

    def __repr__(self) -> str:
        return f"snowmobile.Snowmobile(creds='{self.cfg.connection.creds}')"
