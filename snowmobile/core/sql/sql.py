"""
:mod:`SQL` contains utility methods to generate & execute common SQL commands.

note:
    *   The :attr:`auto_run` attribute defaults to `True`, meaning that the
        generated sql will execute when a method is called; if set to `False`
        the method will return the sql as a string without executing.
    *   The :class:`SQL` object is primarily interacted with as a
        pre-instantiated attribute of :class:`Connector`; in these instances
        users can fetch the generated sql as a string either by:
            1.  Providing *run=False* to any method called; this will override
                all behavior set by the current value of :attr:`auto_run`.
            2.  Setting the :attr:`auto_run` attribute to `False` on an existing
                instance of :class:`SQL`, which will replicate the behavior of
                `(1)` without needing to provide *run=False* to each method
                called on that instance. This is illustrated in lines **10**,
                **13**, and **16** of the below example:

                .. literalinclude:: /examples/mod_sql/set_auto_run.py
                   :language: python
                   :lineno-start: 1
                   :emphasize-lines: 10, 13, 16


"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd

from snowmobile.core.utils.parsing import p, strip, up

from ._map_information_schema import MAP_INFORMATION_SCHEMA as INFO


class SQL:
    """SQL class for generation & execution of common sql commands.

    Intended to be interacted with as an attribute of :class:`snowmobile.Connect`.

    note:
        *   All arguments except for :attr:`sn` are optional.
        *   The benefit of setting the other attributes on an instance of :class:`SQL`
            is to (optionally) avoid passing the same information to multiple methods
            when generating a variety of statements around the same object.

    Attributes:
        sn (snowmobile.Connect):
            :class:`snowmobile.Connect` for sql execution and connection information.
        nm (str):
            Object name to use in generated sql (e.g. 'some_table_name')
        obj (str):
            Object type to use in generated sql (e.g. 'table')
        schema (str):
            Schema to use when dot-prefixing sql; defaults to the schema with which the
            :attr:`sn` is connected to.
        auto_run (bool):
            Indicates whether to automatically execute the sql generated by a given
            method; defaults to *True*

    """

    def __init__(
        self,
        sn=None,
        nm: Optional[str] = None,
        obj: Optional[str] = None,
        auto_run: Optional[bool] = True,
    ):
        """Initializes a :class:`snowmobile.SQL` object."""
        self.sn = sn
        schema, nm = p(nm=nm)
        self.nm: str = nm
        self.schema = schema or sn.cfg.connection.current.schema_name
        self.obj: str = obj or "table"
        self.auto_run: bool = auto_run

    def info_schema_tables(
        self,
        nm: Optional[str] = None,
        fields: List[str] = None,
        restrictions: Dict[str, str] = None,
        order_by: List[Optional[str, int]] = None,
        all_schemas: bool = False,
        run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Query ``information_schema.tables`` for a given table or view.

        Args:
            nm (str):
                Table name, including schema if creating a stage outside of the
                current schema.
            fields (List[str]):
                List of fields to include in returned results (e.g.
                ['table_name', 'table_type', 'last_altered'])
            restrictions (List[str]):
                List of conditionals typed as literal components of a `where`
                clause (e.g.
                ["table_type = 'base table'", 'last_altered::date = current_date()']
                ).
            order_by (List[str]):
                List of fields or their ordinal positions to order the results by.
            all_schemas (bool):
                Include tables/views from all schemas; defaults to `False`.
            run (bool):
                Determines whether to run the generated sql or not; defaults to `None`
                which will reference the current value of the :attr:`auto_run` attribute
                which defaults to `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        # fmt: off
        try:
            schema, nm = p(nm)
            table = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )
            schema = self._validate(
                val=(schema or self.schema), nm='schema', attr_nm='schema'
            )
        except ValueError as e:
            raise e
        # fmt: on

        restrictions = {
            **(restrictions or dict()),
            **{
                "lower(table_name)": f"'{table.lower()}'",
                "lower(table_schema)": f"'{schema.lower()}'",
            },
        }
        if all_schemas:
            _ = restrictions.pop("lower(table_schema)")

        sql = self._info_schema_generic(
            obj="table", fields=fields, restrictions=restrictions, order_by=order_by,
        )

        return self.sn.query(sql=sql) if self._run(run) else sql

    def info_schema_columns(
        self,
        nm: Optional[str] = None,
        fields: Optional[List] = None,
        restrictions: Dict = None,
        order_by: Optional[List] = None,
        all_schemas: bool = False,
        run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Query ``information_schema.columns`` for a given table or view.

        Args:
            nm (str):
                Table name, including schema if creating a stage outside of the
                current schema.
            fields (List[str]):
                List of fields to include in returned results (e.g.
                ['ordinal_position', 'column_name', 'data_type'])
            restrictions (List[str]):
                List of conditionals typed as literal components of a `where`
                clause (e.g.["regexp_count(lower(column_name), 'tmstmp') = 0"]).
            order_by (List[str]):
                List of fields or their ordinal positions to order the results by.
            all_schemas (bool):
                Include tables/views from all schemas; defaults to `False`.
            run (bool):
                Determines whether to run the generated sql or not; defaults to `None`
                which will reference the current value of the :attr:`auto_run` attribute
                which defaults to `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        # fmt: off
        try:
            schema, nm = p(nm)
            table = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )
            schema = self._validate(
                val=(schema or self.schema), nm='schema', attr_nm='schema'
            )
        except ValueError as e:
            raise e
        # fmt: on
        restrictions = {
            **(restrictions or dict()),
            **{
                "lower(table_name)": f"'{table.lower()}'",
                "lower(table_schema)": f"'{schema.lower()}'",
            },
        }
        if all_schemas:
            restrictions.pop("lower(table_schema)")

        sql = self._info_schema_generic(
            obj="column", fields=fields, restrictions=restrictions, order_by=order_by,
        )

        return self.sn.query(sql=sql) if self._run(run) else sql

    def cnt_records(self, nm: Optional[str] = None, run: bool = None):
        """Number of records within a table or view.

        Args:
            nm (str):
                Table name, including schema if creating a stage outside of the
                current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        try:
            obj_name = self._validate(
                val=(nm or self.nm), nm="obj_name", attr_nm="obj_name"
            )
        except ValueError as e:
            raise e
        sql = f"select count(*) from {obj_name}"
        return self.sn.query(sql=sql) if self._run(run) else sql

    def table_last_altered(
        self, nm: Optional[str] = None, run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Last altered timestamp for a table or view.

        Args:
            nm (str):
                Table name, including schema if creating a stage outside of the
                current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        try:
            sql = self.info_schema_tables(
                nm=nm, fields=["table_name", "table_schema", "last_altered"],
            )
            return self.sn.query(sql=sql) if self._run(run) else sql
        except AssertionError as e:
            raise e

    def create_stage(
        self, nm_stage: str, nm_format: str, replace: bool = False, run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Create a staging table.

        Args:
            nm_stage (str):
                Name of stage to create, including schema if creating a stage
                outside of the current schema.
            nm_format (str):
                Name of file format to specify for the stage, including schema
                if using a format from outside of the current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.
            replace (bool):
                Indicates whether to replace an existing stage if pre-existing;
                default is `False`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        create = self._create(replace=replace)
        _sql = f"{create} stage {nm_stage} file_format = {nm_format};"
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def drop(
        self, nm: Optional[str] = None, obj: Optional[str] = None, run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Drop a ``Snowflake`` object.

        Args:
            nm (str):
                Name of the object to drop, including schema if creating a stage
                outside of the current schema.
            obj (str):
                Type of object to drop (e.g. 'table', 'schema', etc)
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        # fmt: off
        schema, nm = p(nm)
        try:
            obj_schema = self._validate(
                val=(schema or self.schema), nm='obj_schema', attr_nm='schema'
            )
            obj_name = self._validate(
                val=(nm or self.nm), nm='obj_name', attr_nm='obj_name'
            )
            obj = self._validate(
                val=(obj or self.obj), nm='obj', attr_nm='obj'
            )
        except ValueError as e:
            raise e
        # fmt: on
        _sql = (
            f"drop {obj} if exists {up(obj_schema)}.{up(obj_name)}"
            if obj.lower() in ["table", "view", "file_format"]
            else f"drop {obj} if exists {up(obj_name)}"
        )
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def clone(
        self,
        nm: Optional[str] = None,
        to: Optional[str] = None,
        obj: Optional[str] = None,
        run: bool = None,
        replace: bool = False,
    ) -> Union[str, pd.DataFrame]:
        """Clone a ``Snowflake`` object.

        Warnings:
            *   Make sure to read `Snowflake's documentation
                <https://docs.snowflake.com/en/sql-reference/sql/create-clone.html>`_
                for restrictions and considerations when cloning objects.

        Note:
            *   In this specific method, the value provided to ``nm`` and ``to``
                can be a single object name, a single schema, or both in the
                form of `obj_schema.obj_name` depending on the desired outcome.
            *   Additionally, **at least one of the** ``nm`` **or** ``to``
                **arguments must be provided**.
            *   The defaults for the target object are constructed such that
                users can **either**:
                    1.  Clone objects to *other* schemas that inherit the
                        source object's *name* without specifying so in the
                        ``to`` argument, **or**
                    2.  Clone objects within the *current* schema that inherit
                        the source object's *schema* without specifying so in
                        the ``to`` argument.
            *   If providing a schema without a name to either argument, prefix
                the value provided with `__` to signify it's a schema and not
                a lower-level object to be cloned.
                    *   e.g. providing `nm='sample_table'` and
                        `to='__sandbox'` will clone `sample_table` from the
                        current schema to `sandbox.sample_table`.
            *   An assertion error will be raised raised if neither argument
                is specified as *this would result in a command to clone an
                object and store it in an object that has the same name &
                schema as the object being cloned*.

        Args:
            nm (str):
                Name of the object to clone, including schema if cloning an
                object outside of the current schema.
            to (str):
                Target name for cloned object, including schema if cloning an
                object outside of the current schema.
            obj (str):
                Type of object to clone (e.g. 'table', 'view', 'file-format');
                defaults to `table`.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.
            replace (bool):
                Indicates whether to replace an existing stage if pre-existing;
                default is `False`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        schema, nm = p(nm)
        to_schema, to = p(nm=to)
        # fmt: off
        try:
            obj = self._validate(
                val=(obj or self.obj), nm='obj', attr_nm='obj'
            )
            schema = self._validate(
                val=(schema or self.schema), nm='schema', attr_nm='schema'
            )
            nm = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )

            to_schema = to_schema or schema
            to = to or nm
            if not to_schema and not to:
                raise ValueError(
                    "At least one of '__schema' or 'name` must be provided "
                    "in the 'to' argument of sql.clone()."
                )
            if nm == to and schema == to_schema:
                raise ValueError(
                    f"Target object name & schema mirrors source object name/schema. "
                    f"Please provide a different value `to`"
                )
        except ValueError as e:
            raise e
        # fmt: on
        create = self._create(replace=replace)
        _sql = (
            f"{create} {obj} {up(to_schema)}.{up(to)} " f"clone {up(schema)}.{up(nm)}"
        )
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def put_file_from_stage(
        self,
        path: Union[Path, str],
        nm_stage: str,
        options: Dict = None,
        ignore_defaults: bool = False,
        run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Generates a 'put' command into a staging table from a local file.

        Args:
            path (Union[Path, str]):
                Path to local data file as a :class:`pathlib.Path` or string.
            nm_stage (str):
                Name of the staging table to load into.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.
            options (dict):
                Optional arguments to add to `put` statement in addition to
                the values specified in the ``loading-defaults.put`` section
                of **snowmobile.toml**.
            ignore_defaults (bool):
                Option to ignore the values specified in **snowmobile.toml**;
                defaults to `False`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        path = Path(str(path))
        statement = [f"put file://{path.as_posix()} @{nm_stage}"]
        # fmt: off
        defaults = (
            self.sn.cfg.loading.put.dict(by_alias=False) if not ignore_defaults
            else dict()
        )
        options = {
            **defaults,
            **(options or dict()),
        }
        for k, v in options.items():
            statement.append(f"\t{k} = {str(v).lower() if isinstance(v, bool) else v}")
        # fmt: on
        _sql = "\n".join(statement)
        sql = strip(_sql, trailing=False, whitespace=False, blanks=True)

        return self.sn.query(sql=sql) if self._run(run) else sql

    def copy_into_table_from_stage(
        self,
        nm: str,
        nm_stage: str,
        options: Dict = None,
        ignore_defaults: bool = False,
        run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Generates a command to copy data into a table from a staging table.

        Args:
            nm (str):
                Name of the object to drop, including schema if creating a stage
                outside of the current schema.
            nm_stage (str):
                Name of the staging table to load from.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.
            options (dict):
                Optional arguments to add to `put` statement in addition to
                the values specified in the ``loading-defaults.put`` section
                of **snowmobile.toml**.
            ignore_defaults (bool):
                Option to ignore the values specified in **snowmobile.toml**;
                defaults to `False`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        statement = [f"copy into {nm} from @{nm_stage}"]
        defaults = (
            self.sn.cfg.loading.copy_into.dict(by_alias=False)
            if not ignore_defaults
            else dict()
        )
        options = {
            **defaults,
            **(options or dict()),
        }
        for k, v in options.items():
            statement.append(f"\t{k} = {v}")
        _sql = "\n".join(statement)
        sql = strip(_sql, trailing=False, whitespace=False, blanks=True)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def show_file_formats(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Lists all file formats in the current schema.

        Args:
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        sql = f"show file formats"
        return self.sn.query(sql=sql) if self._run(run) else sql

    def ddl(
        self, nm: Optional[str] = None, obj: Optional[str] = None, run: bool = None,
    ) -> str:
        """Query the DDL for an in-warehouse object.

        Args:
            nm (str):
                Name of the object to get DDL for, including schema if object
                is outside of the current schema.
            obj (str):
                Type of object to get DDL for (e.g. 'table', 'view', 'file-format').
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (str):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        schema, nm = p(nm)
        try:
            obj = self._validate(val=(obj or self.obj), nm="obj", attr_nm="obj")
            schema = self._validate(
                val=(schema or self.schema), nm="schema", attr_nm="schema"
            )
            nm = self._validate(val=(nm or self.nm), nm="nm", attr_nm="nm")
        except ValueError as e:
            raise e
        _sql = f"select get_ddl('{obj}', '{up(schema)}.{up(nm)}') as ddl"
        sql = strip(_sql)
        return self.sn.query(sql=sql).snowmobile.to_list(n=1) if self._run(run) else sql

    def table_sample(
        self, nm: Optional[str] = None, n: Optional[int] = None, run: bool = None,
    ) -> Union[str, pd.DataFrame]:
        """Select `n` sample records from a table.

        Args:
            nm (str):
                Name of table or view to sample, including schema if the table
                or view is outside of the current schema.
            n (int):
                Number of records to return, implemented as a 'limit' clause
                in the query; defaults to 1.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        schema, nm = p(nm)
        # fmt: off
        try:
            schema = self._validate(
                val=(schema or self.schema), nm='schema', attr_nm='schema'
            )
            table = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )
        except ValueError as e:
            raise e
        # fmt: on
        _sql = f"""
select
    *
from {up(schema)}.{up(table)}
limit {n or 1}
        """
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def truncate(self, nm: str, run: bool = None) -> Union[str, pd.DataFrame]:
        """Truncate a table.

        Args:
            nm (str):
                Name of table, including schema if the table is outside of the
                current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        schema, nm = p(nm)
        # fmt: off
        try:
            schema = self._validate(
                val=(schema or self.schema), nm='schema', attr_nm='schema'
            )
            name = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )
        except ValueError as e:
            raise e
        # fmt: on
        _sql = f"truncate table {up(schema)}.{up(name)}"
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def current(self, obj: str, run: bool = None):
        """Generic implementation of 'select current' for session-based objects.

        Args:
            obj (str):
                Type of object to retrieve information for (schema, session, ..).
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        _sql = f"select current_{obj}()"
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def current_session(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Select the current session."""
        return self.current(obj="session", run=run)

    def current_schema(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Select the current schema."""
        return self.current(obj="schema", run=run)

    def current_database(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Select the current database."""
        return self.current(obj="database", run=run)

    def current_warehouse(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Select the current warehouse."""
        return self.current(obj="warehouse", run=run)

    def current_role(self, run: bool = None) -> Union[str, pd.DataFrame]:
        """Select the current role."""
        return self.current(obj="role", run=run)

    def use(self, nm: str, obj: str, run: bool = None):
        """Generic implementation of 'use' command for in-warehouse objects.

        Args:
            nm (str):
                Name of object to use (schema name, warehouse name, role name, ..).
            obj (str):
                Type of object to use (schema, warehouse, role, ..).
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, pd.DataFrame]):
            Either:
                1.  The results of the query as a :class:`pandas.DataFrame`, or
                2.  The generated query as a :class:`str` of sql.

        """
        # fmt: off
        try:
            name = self._validate(
                val=(nm or self.nm), nm='nm', attr_nm='nm'
            )
        except ValueError as e:
            raise e
        # fmt: on
        _sql = f"use {obj} {up(name)}"
        sql = strip(_sql)
        return self.sn.query(sql=sql) if self._run(run) else sql

    def use_schema(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, pd.DataFrame]:
        """Use schema command."""
        return self.use(obj="schema", nm=nm, run=run)

    def use_database(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, pd.DataFrame]:
        """Use database command."""
        return self.use(obj="database", nm=nm, run=run)

    def use_warehouse(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, pd.DataFrame]:
        """Use warehouse command."""
        return self.use(obj="warehouse", nm=nm, run=run)

    def use_role(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, pd.DataFrame]:
        """Use role command."""
        return self.use(obj="role", nm=nm, run=run)

    def columns(
        self,
        nm: Optional[str] = None,
        from_info_schema: bool = False,
        run: bool = None,
    ) -> Union[str, List]:
        """Returns an ordered list of columns for a table or view.

        note:
            *   The default behavior of this method is to retrieve the columns
                for a table or view by selecting a single sample record
                from the table and extracting the column names directly off
                the returned :class:`pandas.DataFrame` due to the performance
                gains in selecting a sample record as opposed to querying the
                ``information_schema.columns``.
            *   This can be changed by passing `from_info_schema=False`.

        Args:
            nm (str):
                Name of table or view, including schema if the table or view is
                outside of the current schema.
            from_info_schema (bool):
                Indicates whether to retrieve columns via the
                ``information_schema.columns`` or by selecting a sample record
                from the table or view; defaults to `False`.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, List]):
            Either:
                1.  An ordered list of columns for the table or view, **or**
                2.  The query against the table or view as a :class:`str` of sql.

        """
        if from_info_schema:
            return self._columns_from_info_schema(nm=nm, run=run)
        else:
            return self._columns_from_sample(nm=nm, run=run)

    # noinspection PyBroadException
    def exists(self, nm: Optional[str] = None) -> bool:
        """Checks the existence of a table or view.

        Args:
            nm (str):
                Name of table or view, including schema if the table or view is
                outside of the current schema.

        Returns (bool):
            Boolean indication of whether or not the table or view exists.

        """
        try:
            _ = self.table_sample(nm=nm)
            return True
        except:
            return False

    def _columns_from_info_schema(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, List]:
        """Retrieves list of columns for a table or view **from information schema**.

        Args:
            nm (str):
                Name of table or view, including schema if the table or view is
                outside of the current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, List]):
            Either:
                1.  An ordered list of columns for the table or view, **or**
                2.  The query against ``information_schema.columns`` as a
                    :class:`str` of sql.

        """
        sql = self.info_schema_columns(
            nm=nm, fields=["ordinal_position", "column_name"], order_by=[1], run=False,
        )
        return self.sn.query(sql).snowmobile.to_list(col="column_name") if run else sql

    def _columns_from_sample(
        self, nm: Optional[str] = None, run: bool = None
    ) -> Union[str, List]:
        """Retrieves a list of columns for a table or view from **sampling table**.

        Args:
            nm (str):
                Name of table or view, including schema if the table or view is
                outside of the current schema.
            run (bool):
                Indicates whether to execute generated sql or return as string;
                default is `True`.

        Returns (Union[str, List]):
            Either:
                1.  An ordered list of columns for the table or view, **or**
                2.  The query against the table or view as a :class:`str` of sql.

        """
        _sql = self.table_sample(nm=nm, run=False, n=1)
        sql = strip(_sql)
        return list(self.sn.query(sql, lower=False).columns) if self._run(run) else sql

    @staticmethod
    def _create(replace: bool = False):
        """Utility to generate 'create'/'create or replace' based on an argument."""
        return "create" if not replace else "create or replace"

    def _run(self, run: Union[bool, None]) -> bool:
        """Determines whether or not to execute a piece of sql.

        Used in all subsequent methods containing a `run` argument.

        Args:
            run (Union[bool, None]):
                The value from a method's `run` argument.

        Returns (bool):
            Boolean value indicating whether or not to execute the sql generated by
            the method to which the value of `run` was passed.

        note:
            *   The default value of `run` in all subsequent methods is ``None``.
            *   When any method of :class:`SQL` containing a `run` argument is called,
                the argument's value is passed to this method which returns either:
                    1.  The argument's value if it is a valid bool (i.e. a user-provided
                        value to the method), or
                    2.  The boolean representation of the current :attr:`auto_run`
                        attribute (`True` by default).

        """
        if isinstance(run, bool):
            return run
        else:
            return bool(self.auto_run)

    def _info_schema_generic(
        self,
        obj: str,
        fields: List[str] = None,
        restrictions: Dict[str, str] = None,
        order_by: Optional[List] = None,
    ) -> str:
        """Generic case of selecting from information schema tables/columns.

        Queries different parts of the information schema based on an ``obj``
        and the mapping of object type to information schema defined in
        `snowmobile.core.sql._map_information_schema.py`.

        """
        # fmt: off
        if obj in INFO.values():
            obj = {v: k for k, v in INFO.items()}[obj]
        if obj not in INFO.keys():
            raise ValueError(
                f"\nobj='{obj}' is not a supported object type for the"
                f" information_schema method called.\n"
                f"Supported objects are:\n\t[{','.join(INFO.keys())}]"
            )
        # fmt: on

        info_schema_loc = INFO[obj]
        fields = self.fields(fields=fields)
        where = self.where(restrictions=restrictions)
        order_by = self.order(by=order_by)

        sql = f"""
select 
{fields}
from information_schema.{info_schema_loc}
{where}
{order_by}
"""
        return strip(sql, trailing=False, blanks=True)

    @staticmethod
    def order(by: List[Union[int, str]]) -> str:
        """Generates 'order by' clause from a list of fields or field ordinal positions."""
        if by:
            order_by_fields = ",".join(str(v) for v in by)
            return f"order by {order_by_fields}"
        else:
            return str()

    @staticmethod
    def where(restrictions: Dict) -> str:
        """Generates a 'where' clause based on a dictionary of restrictions.

        Args:
            restrictions (dict):
                A dictionary of conditionals where each key/value pair
                respectively represents the left/right side of a condition
                within a 'where' clause.

        Returns (str):
            Formatted where clause.

        """
        if restrictions:
            args = [
                f"{str(where_this)} = {str(equals_this)}"
                for where_this, equals_this in restrictions.items()
            ]
            args = "\n\tand ".join(args)
            return f"where\n\t{args}"
        else:
            return str()

    @staticmethod
    def fields(fields: List) -> str:
        """Utility to generate fields within a 'select' statement."""
        return "\n".join(
            f'\t{"," if i > 1 else ""}{f}'
            for i, f in enumerate(fields or ["*"], start=1)
        )

    @staticmethod
    def _validate(
        val: Optional[str, int], nm: str, attr_nm: Optional[str] = None
    ) -> str:
        """Validates the value of an argument passed to a method.

        This method is built to validate method arguments in instances where an
        unspecified argument can fall back to an attribute if it has been set.

        Each of the 'closing' variables below represents a different ending to
        a sentence within the exception message depending on the value provided
        from the method and if the attribute the argument falls back to has been
        set at the time the method is called.

        Args:
            val (Union[str, int]:
                Value to validate.
            nm (str):
                Name of argument in the method being called.
            attr_nm (str):
                Name of attribute to fall back to if the boolean representation
                of ``val`` is `False`.

        """
        if not val:
            closing1 = (
                "." if not attr_nm else f", nor is its fallback attribute '{attr_nm}'."
            )
            closing2 = (
                "."
                if not attr_nm
                else f" or set the '{attr_nm}' attribute before calling the method."
            )
            raise ValueError(
                f"\nValue provided for '{nm}' is not valid{closing1}\n"
                f"Please provide a valid value for '{nm}'{closing2}"
            )
        return val

    def _reset(self):
        self.schema = self.sn.cfg.connection.current.schema_name
        self.nm = None
        self.obj = "table"
        return self

    def __copy__(self) -> SQL:
        return type(self)(sn=self.sn, nm=f"{self.schema}.{self.nm}", obj=self.obj,)

    def copy(self) -> SQL:
        return self.__copy__()

    def __call__(self, *args, **kwargs) -> SQL:
        for k, v in kwargs.items():
            if k in vars(self):
                setattr(self, k, v)
        return self

    def __getitem__(self, item):
        return vars(self)[item]

    def __getattr__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __str__(self) -> str:
        return f"snowmobile.SQL(creds='{self.sn.cfg.connection.creds}')"

    def __repr__(self) -> str:
        return f"snowmobile.SQL(creds='{self.sn.cfg.connection.creds}')"
