"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any, ContextManager, Dict, Set, Union, Callable

import pandas as pd
import sqlparse
from IPython.core.display import Markdown, display

from snowflake.connector.errors import ProgrammingError, DatabaseError
from pandas.io.sql import DatabaseError as pdDataBaseError

from snowmobile.core.configuration import Pattern
from snowmobile.core.markup.section import Section
from snowmobile.core import Connector
from .errors import StatementInternalError
from .tag import Tag


class Statement:
    """Base class for all :class:`Statement` objects.

    Home for attributes and methods that are associated with **all** statement
    objects, generic or QA.

    Attributes:
        sn (snowmobile.Connect):
            :class:`snowmobile.Connect` object.
        statement (Union[sqlparse.sql.Statement, str]):
            A :class:`sqlparse.sql.Statement` object.
        index (int):
            The context-specific index position of a statement within a script;
            can be `None`.
        _index (int):
            The original index position of a statement as read from the source;
            This is used to restore the index position of a given statement
            before exiting a specified context within :class:`snowmobile.Script`.
        patterns (config.Pattern):
            :class:`config.Pattern` object for more succinct access to
            values specified in **snowmobile.toml**.
        results (pd.DataFrame):
            The results of the statement if executed as a :class:`pandas.DataFrame`.
        outcome (int):
            Numeric indicator of outcome; defaults to `0` and is modified
            based on the outcome of statement execution and/or QA validation
            for derived classes.
        outcome_txt (str):
            Plain text of outcome ('skipped', 'failed', 'completed', 'passed').
        outcome_html (str):
            HTML text for the outcome as an admonition/information banner
            based on the following mapping of :attr:`outcome_txt` to
            admonition argument:
                *   `failed` ------> `warning`
                *   `completed` --> `info`
                *   `passed` -----> `success`
        start_time (int):
            Unix timestamp of the query start time if executed; 0 otherwise.
        end_time (int):
            Unix timestamp of the query end time if executed; 0 otherwise.
        execution_time (int):
            Execution time of the query in seconds if executed; 0 otherwise.
        execution_time_txt (str):
            Plain text description of execution time if executed; returned in
            seconds if execution time is less than 60 seconds, minutes otherwise.
        attrs_raw (str):
            A raw string of the tag/attributes associated with the statement.
        attrs_parsed (dict):
            A parsed dictionary of the tag/attributes associated with the statement.
        is_tagged (bool):
            Indicates whether or not the statement is tagged by the user.
        is_multiline (bool):
            Indicates whether or not a statement tag is a multiline tag; will
            be `False` by default if :attr:`is_tagged` is `False`.
        first_keyword (sqlparse.sql.Token):
            The first keyword within the statement as a :class:`sqlparse.sql.Token`.
        sql (str):
            The sql associated with the statement as a raw string.
        tag (Tag):
            :class:`Tag` object associated with the statement.

    """

    # fmt: off
    _PROCESS_OUTCOMES: Dict[Any, Any] = {
        -3: ("success", "passed"),
        -2: ("warning", "failed"),
        -1: ("-", "error: post-processing"),
        0: ("-", ""),
        1: ("-", "error: execution"),
        2: ("success", "completed"),
    }
    # fmt: on

    # noinspection PyTypeChecker,PydanticTypeChecker
    def __init__(
        self,
        sn: Connector,
        statement: Union[sqlparse.sql.Statement, str],
        index: int = None,
        attrs_raw: str = None,
        **kwargs,
    ):
        self._index: int = index
        self._exclude_attrs = []

        self._tmstmp: int = None
        self.timestamps: Set[int] = set()
        # self._errors: Dict[str, Dict[int, Exception]] = dict()

        self.errors: Dict[int, Dict[int, Exception]] = {}
        self.error_last: Dict[int, Exception] = {}
        self.enc_exception: bool = bool()

        self._outcome: int = int()
        self.outcome: bool = True

        self.executed: bool = bool()

        self.sn = sn
        self.statement: sqlparse.sql.Statement = sn.cfg.script.ensure_sqlparse(
            statement
        )

        self.index: int = index or int()
        self.patterns: Pattern = sn.cfg.script.patterns
        self.results: pd.DataFrame = pd.DataFrame()

        self.start_time: int = int()
        self.end_time: int = int()
        self.execution_time: int = int()
        self.execution_time_txt: str = str()

        self.attrs_raw = attrs_raw or str()
        self.is_tagged: bool = bool(self.attrs_raw)

        # TODO: Make this a single static method from cfg.script
        self.first_keyword = self.statement.token_first(skip_ws=True, skip_cm=True)
        self.sql = sn.cfg.script.isolate_sql(s=self.statement)

        self.tag: Tag = None
        self.attrs_parsed = self.parse()

    @property
    def is_multiline(self) -> bool:
        """Indicates if provided statement tag is a multiline tag."""
        return "\n" in self.attrs_raw

    def parse(self) -> Dict:
        """Parses a statement tag into a valid dictionary.

        Uses the values specified in **snowmobile.toml** to parse a
        raw string of statement arguments into a valid dictionary.

        note:
            *   If :attr:`is_multiline` is `True` and `name` is not included
                within the arguments, an assertion error will be thrown.
            *   If :attr:`is_multiline` is `False`, the raw string within
                the tag will be treated as the name.
            *   The :attr:`tag` attribute is set once parsing is completed
                and name has been validated.

        Returns (dict):
            Parsed tag arguments as a dictionary.

        """
        if self.is_multiline:
            attrs_parsed = self.sn.cfg.script.parse_str(block=self.attrs_raw)
            parsed_contains_name, msg = self._validate_parsed(attrs_parsed=attrs_parsed)
            if not parsed_contains_name:
                raise ValueError(msg)
            name = attrs_parsed.pop("name")
        else:
            attrs_parsed, name = dict(), self.attrs_raw

        self.set_tag(nm_pr=name)

        return attrs_parsed

    def set_tag(self, nm_pr: str) -> None:
        """Sets the :attr:`tag` attribute post-parsing of arguments.

        Args:
            nm_pr (str):
                Tag name; will be blank if no tag is provided.
        """
        self.tag: Tag = Tag(
            index=self.index,
            sql=self.sql,
            nm_pr=nm_pr,
            configuration=self.sn.cfg,
            first_keyword=str(self.first_keyword),
        )

    def start(self):
        """Sets :attr:`start_time` attribute."""
        self.start_time = time.time()

    def end(self):
        """Updates execution time attributes.

        In total, sets:
            *   :attr:`end_time`
            *   :attr:`execution_time`
            *   :attr:`execution_time_txt`

        """
        self._outcome, self.outcome, self.executed = 2, True, True
        self.end_time = time.time()
        self.execution_time = int(self.end_time - self.start_time)
        self.execution_time_txt = (
            f"{self.execution_time}s"
            if self.execution_time < 60
            else f"{int(self.execution_time/60)}m"
        )

    def dump_namespace(self) -> Dict:
        """Parses namespace for attributes specified in **snowmobile.toml**.

        Searches attributes for those matching the keys specified in
        ``script.markdown.attributes.aliases`` within **snowmobile.toml**
        and adds to the existing attributes stored in :attr:`attrs_parsed`
        before returning.

        Returns (dict):
            Combined dictionary of statement attributes from those explicitly
            provided within the script and from object's namespace if specified
            in **snowmobile.toml**.

        """

        config_namespace = self.sn.cfg.script.markdown.attrs.from_namespace
        current_namespace = {
            **self.sn.cfg.attrs_from_obj(obj=self),
            **self.sn.cfg.methods_from_obj(obj=self),
        }
        attrs_to_dump = (
            set(current_namespace)
            .intersection(config_namespace)
            .difference(self._exclude_attrs)
        )

        attrs = self.attrs_parsed
        for k in attrs_to_dump:
            attr = current_namespace[k]
            attr_value = attr() if isinstance(attr, Callable) else attr
            if attr_value:
                attrs[k] = attr_value
        return attrs

    def trim(self) -> str:
        """Statement as a string including only the sql and a single-line tag name.

        note:
            The tag name used here will be the user-provided tag from the
            original script or a generated :attr:`Tag.nm` of a tag was not
            provided for a given statement.

        """
        patterns = self.sn.cfg.script.patterns
        open_p, close_p = patterns.core.to_open, patterns.core.to_close
        return f"{open_p}{self.tag.nm}{close_p}\n{self.sql};\n"

    def render(self) -> None:
        """Renders the statement's sql as markdown in Notebook/IPython environments."""
        display((Markdown(self.as_section().sql_md),))

    @property
    def name(self):
        """Quick access to tag name directly off the :class:`Statement`.."""
        return self.tag.nm

    @property
    def is_derived(self):
        """Indicates whether or not it's a generic or derived (QA) statement."""
        return self.tag.anchor in self.sn.cfg.QA_ANCHORS

    @property
    def lines(self) -> int:
        """Depth of the statement's sql by number of lines."""
        return len(self.sql.split("\n"))

    def as_section(self) -> Section:
        """Returns current statement as a :class:`Section` object."""
        return Section(
            h_contents=self.tag.nm,
            index=self.index,
            parsed=self.dump_namespace(),
            sql=self.sql,
            config=self.sn.cfg,
            results=self.results,
        )

    def set_state(self, tmstmp: int = None, filters: dict = None) -> None:
        """Sets current state/context on a statement object.

        Args:
            tmstmp (int):
                Unix timestamp the :meth:`script.filter()` context manager was
                invoked.
            filters (dict):
                Kwargs passed to :meth:`script.filter()`.

        """
        if tmstmp:
            self.reset(tmstmp=True)
            self._tmstmp = tmstmp
        if filters:
            self.tag.scope(**filters)

    def index_to(self, index: int) -> Statement:
        """Sets the index of the current statement to a specific value.

        Invoked from within :class:`snowmobile.Script` when operating on a
        script within a given context; changes index on the statement object
        and the index stored within the :attr:`tag` attribute.

        Args:
            index (int):
                Integer to set as the statement's index..

        Returns (Statement):
            Current :class:`Statement` object reflecting the revised index.

        """
        self.index = index
        self.tag.index = index
        return self

    def reset(
        self,
        index: bool = False,
        scope: bool = False,
        tmstmp: bool = False,
        errors: bool = False,
    ) -> Statement:
        """Resets statement object to its original state as read from source.

        This includes:
            *   Resetting the statement's index to its original value.
            *   Resetting the statement *tag's* index to its original value.
            *   Resetting the :attr:`is_included` attribute of the statement's
                :attr:`tag` to `True`.

        """
        if index:
            self.index = self._index
            self.tag.index = self._index
        if scope:
            self.tag.is_included = True
        if errors:
            self.error_last = self.exceptions(from_tmstmp=self._tmstmp)
        if tmstmp:
            self.timestamps.add(self.tmstmp)
            self._tmstmp = None
        return self

    def process(self):
        """Used by derived classes for validation logic of the returned results."""
        return self

    @contextmanager
    def _run(
        self, results: bool = True, lower: bool = True, **kwargs,
    ) -> ContextManager[Statement]:
        """Executes statement; used by generic case and derived classes.

        note:
            *   Will only execute sql if the :class:`Statement` object's boolean
                representation (determined by its current scope) evaluates to `True`.
            *   If `results=True`, the results returned are stored within the
                :attr:`results` attribute, not returned directly from this method.

        Args:
            results (bool):
                Whether or not to return results; default is `True`.
            lower (bool):
                Whether or not to lower-case the columns on the returned
                :class:`pandas.DataFrame` if `results=True`.
            render (bool):
                Whether or not to render the sql being executed; useful in
                notebooks when wanting to render the syntax-highlighted sql
                while executing a statement.
            **kwargs:
                Included for compatibility purposes with derived classes.

        Returns (Statement):
            The :class:`Statement` object itself post-executing or skipping
            execution of the sql based on its current scope.

        """
        try:
            if self:
                self.start()
                self.results = self.sn.query(self.sql, results=results, lower=lower)
                self.end()
            yield self

        except (ProgrammingError, pdDataBaseError, DatabaseError):
            self._exception(e=self.sn.error, _id=1)
            yield

        finally:
            # only post-process when execution did not raise database error
            if self._outcome == 2:
                self.process()

            return self

    def run(
        self,
        results: bool = True,
        lower: bool = True,
        render: bool = False,
        on_error: str = None,
        on_exception: str = None,
        on_failure: str = None,
        tmstmp: int = None,
        **kwargs,
    ) -> Statement:
        """Run method for all statement objects.

        Args:
            results (bool):
                Store results of query in :attr:`results`.
            lower (bool):
                Lower case column names in :attr:`results` DataFrame if
                `results=True`.
            render (bool):
                Render the sql executed as markdown.
            on_error (str):
                *   `e`: exception
                *   `c`: continue
            tmstmp (str):
                Unix timestamp of the current context initialization.
            **kwargs:
                Keyword arguments for :meth:`update()` and compatibility with
                derived classes.

        Returns (Statement):
            Statement object post-executing query.

        """

        if tmstmp and self._tmstmp != tmstmp:
            self.set_state(tmstmp=tmstmp)
        elif not tmstmp and not self._tmstmp:
            self.set_state(tmstmp=self.tmstmp)

        with self._run(results=results, lower=lower, **kwargs) as r:
            pass

        # ---------------------------
        if (
            not self.is_derived      # is generic statement
            and self._outcome == 1   # database error raised during execution
            and on_error != "c"      # stop on execution error
        ):
            self.exceptions(last=True, _raise=True)
            raise self.exceptions(last=True)
        # ---------------------------
        if (
            self.is_derived          # is child class with `.process()` method
            and self._outcome == -1  # exception thrown during post-processing
            and on_exception != "c"  # stop on post-processing exception
        ):
            self.exceptions(last=True, _raise=True)
        # ---------------------------
        if (
            self.is_derived          # is child class with `.process()` method
            and self._outcome == -2  # outcome of `.process()` did not pass
            and on_failure != "c"    # stop on failure of `.process()`
        ):
            self.exceptions(last=True, _raise=True)
        # ---------------------------

        if render:
            self.render()

        return self

    @property
    def tmstmp(self):
        """Returns timestamp id of current context."""
        if not self._tmstmp:
            self._tmstmp = int(time.time())
        return self._tmstmp

    @staticmethod
    def _validate_parsed(attrs_parsed: Dict):
        """Returns args to verify 'name' attribute is present in a multiline tag."""
        condition, msg = (
            attrs_parsed.get("name"),
            f"Required attribute 'name' not found in multi-line tag's "
            f"arguments;\n attributes found are: {','.join(list(attrs_parsed))}",
        )
        return condition, msg

    # confusing part is that this sets outcome and logs exception
    def _exception(self, _id: int, e: Exception, _raise: bool = False) -> None:
        """Saves exception encountered; will raise if `_raise=False` is passed."""
        self._outcome = _id
        current_total = self.errors[self._tmstmp] if self._tmstmp in self.errors else dict()
        current_total[int(time.time())] = e
        self.errors[self._tmstmp] = current_total
        if _raise:
            raise e

    def exceptions(
        self, last: bool = False, hist: bool = False, _raise: bool = False,
        from_tmstmp: int = None,
    ):
        """All exceptions encountered, sorted from most to least recent."""
        if from_tmstmp:
            return self.errors.get(from_tmstmp)

        if not self._tmstmp:
            raise StatementInternalError(
                nm='statement._tmstmp = None',
                msg=(
                    'a call was made to `statement.exceptions()` while the '
                    'current value of `statement._tmstmp` is None.'
                )
            )
        elif not self.errors.get(self._tmstmp):
            raise StatementInternalError(
                nm='statement._tmstmp not in statement.errors',
                msg=(
                    'a call was made to `statement.exceptions()` without the '
                    'current statement._tmstmp existing in statement.errors.'
                )
            )

        if hist:
            return self.errors

        total = {
            tmstmp: e
            for tmstmp, e in self.errors[self._tmstmp].items()
        }
        sorted_total = {i: total[i] for i in sorted(total, reverse=True)}

        if not last:
            return sorted_total
        elif not _raise:
            return sorted_total[max(sorted_total)]
        else:
            raise sorted_total[max(sorted_total)]

    def outcome_txt(self, _id: int = None) -> str:
        """Outcome as a string."""
        return self._PROCESS_OUTCOMES[_id or self._outcome][1]

    @property
    def outcome_html(self) -> str:
        """Outcome as an html admonition banner."""
        alert = self._PROCESS_OUTCOMES[self._outcome][0]
        return f"""
<div class="alert-{alert}">
<center><b>====/ {self.outcome_txt()} /====</b></center>
</div>""".strip()

    def __bool__(self):
        """Determined by the value of :attr:`Tag.is_included`."""
        return self.tag.is_included

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __str__(self) -> str:
        return f"Statement('{self.tag.nm}')"

    def __repr__(self) -> str:
        return f"Statement('{self.tag.nm}')"
