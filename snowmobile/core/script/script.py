"""
Class for intraacting with Script objects.

These are intended to be instantiated from a local *.sql* file or a readable
text file containing sql code. The :meth:`Script.read(from_str=True)` option
was included for the purposes of creating easily reproducible examples of how a
script is parsed.

# TODO: Add an example of how to re-implement the execute_stream() method from
#   snowflake.Connector for documentation.
"""
from __future__ import annotations

import collections
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ContextManager, Dict, List, Optional, Set, Tuple, Union

import sqlparse

from snowmobile.core import Connector, Doc, configuration
from snowmobile.core.configuration.schema import Marker
from snowmobile.core.statement import Diff, Empty, Statement
from ._stdout import Script as Stdout


class Script:

    # Maps statement anchors to alternate base class.
    _ANCHOR_TO_QA_BASE_MAP = {
        "qa-diff": Diff,
        "qa-empty": Empty,
    }

    def __init__(
        self, sn: Connector, path: Union[Path, str] = None, as_generic: bool = False
    ):
        self._is_from_str: bool = bool()
        self._statements_parsed: Dict[int, sqlparse.sql.Statement] = dict()
        self._statements_all: Dict[int, Statement] = dict()
        self._open = sn.cfg.script.patterns.core.to_open
        self._close = sn.cfg.script.patterns.core.to_close

        self.sn: Connector = sn
        self.patterns: configuration.schema.Pattern = sn.cfg.script.patterns
        self.as_generic = as_generic
        self.filters: Dict[Any[str, int], Dict[str, Set]] = {
            int(): {k: v for k, v in self.sn.cfg.scopes.items() if v}
        }
        self.filtered: bool = bool()

        self.intra_statement_marker_hashmap_idx: Dict = dict()
        self.intra_statement_marker_hashmap_txt: Dict = dict()
        self.all_marker_hashmap: Dict = dict()
        self.markers: Dict[int, Marker] = dict()

        if path:
            try:
                self.read(path=path)
            except IOError as e:
                raise e
        else:
            self.path: Path = path
            self.name: str = str()
            self.source: str = str()

        if self.source:
            self._parse_statements()

        self._stdout: Stdout = Stdout(name=self.name, statements=dict())

    def _post_source__init__(self, from_str: bool = False) -> Script:
        """Sets final attributes and parses source once provided."""
        self.name = self.path.name
        self._is_from_str = from_str
        try:
            self._parse()
        except Exception as e:
            raise e
        return self

    def read(self, path: Path = None) -> Script:
        """Runs quick path validation and reads in a sql file as a string.

        A valid `path` must be provided if the `script.path` attribute hasn't
        been set; ``ValueErrors`` will be thrown if neither is valid.

        Args:
            path (pathlib.Path):
                Full path to a sql object.

        """
        path = Path(str(path)) if path else self.path
        # fmt: off
        if not path.exists():
            raise IOError(
                f"{path} does not exist; `path` must be a valid file path."
            )
        if not path.is_file():
            raise IOError(
                f"`path` argument must map to a file, not a directory."
            )
        # fmt: on
        self.path: Path = Path(str(path))
        with open(self.path, "r") as r:
            self.source = r.read()
        return self._post_source__init__()

    def from_str(self, sql: str, name: str, directory: Path = Path.cwd()) -> Script:
        """Instantiates a raw string of sql as a script."""
        # fmt: off
        if not name.endswith(".sql"):
            raise ValueError(
                f"`name` must end in .sql; '{name}' provided."
            )
        # fmt: on
        self.path: Path = Path(str(directory)) / name
        self.source = sql
        return self._post_source__init__(from_str=True)

    @property
    def source_stream(self) -> sqlparse.sql.Statement:
        """Parses source sql into individual statements."""
        for s in sqlparse.parsestream(stream=self.source):
            if self.sn.cfg.script.is_valid_sql(s=s):
                yield s

    def add_statement(
        self, s: Union[sqlparse.sql.Statement, str], index: int = None
    ) -> None:
        """Adds a statement object to the script.

        Default behavior will only add ``sqlparse.sql.Statement`` objects
        returned from ``script.source_stream``.

        ``clean_parse()`` utility function is utilized so that generated sql
        within Python can be inserted back into the script as raw strings.

        Args:
            s (Union[sqlparse.sql.Statement, str]):
                A sqlparse.sql.Statement object or a raw string of SQL for an
                individual statement.
            index (int):
                Index position of the statement within the script; defaults
                to ``n + 1`` if index is not provided where ``n`` is the number
                of statements within the script at the time ``add_statement()``
                is called.

        """
        index = index or self.depth + 1
        s: sqlparse.sql.Statement = self.sn.cfg.clean_parse(sql=s)

        markers, attrs_raw = self.sn.cfg.script.split_sub_blocks(s=s)
        self._log_markers(idx=index, markers=markers)
        self._add_statement(s=s, index=index, attrs_raw=attrs_raw)

    def _add_statement(
        self, s: sqlparse.sql.Statement, index: int, attrs_raw: str
    ) -> None:
        """Adds a statement object to the script.

        Instantiates a generic statement object, immediately stores by index if
        it's anchor indicates that it's not intended to be a QA statement,
        otherwise instantiates the associated QA statement and stores that
        instead.

        Args:
            s (sqlparse.sql.Statement):
                sqlparse Statement object.
            index (int):
                Statement's index position within script.
            attrs_raw (str):
                Raw string of attributes parsed from the statement.

        """
        # generic case
        statement: Any[Statement, Empty, Diff] = Statement(
            sn=self.sn, statement=s, index=index, attrs_raw=attrs_raw,
        )
        if not statement.is_derived or self.as_generic:
            self._statements_all[index] = statement
        # mapping to associated QA base class otherwise
        else:
            self._statements_all[index] = self._derive_qa_from_generic(
                s=s, generic=statement
            )

    def _log_markers(self, idx: int, markers: List[str]) -> None:
        """Stores intra-statement markers.

        Args:
            idx (int):
                Statement index.
            markers (List[str]):
                List of markers as raw strings found above the statement.
        """
        for i, m in enumerate(markers, start=1):
            _hash = hash(m)
            marker_index = idx + (i / 10)
            self.intra_statement_marker_hashmap_idx[_hash] = marker_index
            self.intra_statement_marker_hashmap_txt[_hash] = m

    def _derive_qa_from_generic(
        self, s: sqlparse.sql.Statement, generic: Statement
    ) -> Union[Diff, Empty]:
        """Instantiates a QA statement object based off the statement's anchor."""
        qa_base_class = self._ANCHOR_TO_QA_BASE_MAP[generic.tag.anchor]
        return qa_base_class(
            sn=self.sn, statement=s, index=generic.index, attrs_raw=generic.attrs_raw,
        )

    def _parse_statements(self) -> None:
        """Instantiates statement objects for all statements in source sql."""
        self._statements_all.clear()
        parsed = self.source_stream
        for i, s in enumerate(parsed, start=1):
            self.add_statement(s=s, index=i)

    def _parse_markers(self):
        """Parses all markers into a hashmap to the raw text within the marker."""
        blocks = self.sn.cfg.script.find_tags(sql=self.source)
        marker_blocks = [
            m
            for m in blocks.values()
            if self.sn.cfg.script.is_marker(m)
            # if p.is_marker(m)
        ]
        self.all_marker_hashmap = {hash(v): v for v in marker_blocks}

    def _parse(self):
        """Parses statements and markers within :attr:`source`."""
        try:
            self._parse_statements()
            self._parse_markers()
            self._merge_markers()
        except Exception as e:
            raise e

    @property
    def _latest_scope_id(self) -> Any[int, str]:
        """Utility property to fetch the ID of the last scope created."""
        return list(self.filters)[-1]

    def _scope_from_id(self, _id: Any[int, str], pop: bool = True) -> Dict:
        """Returns dictionary of scope arguments given an ``_id``.

        Will return scope arguments from ``script.filters`` if ``_id`` is
        pre-existing and template value if not.

        Args:
            _id (Any[int, str]):
                Integer or string value for scope ``ID``.
            pop (bool):
                Remove scope from ``script.scope`` before returning;
                default=False.

        Returns (dict):
            A dictionary of scope keys to associated values.

        """
        template = self.sn.cfg.scopes
        if _id not in self.filters:
            return template
        else:
            scope = self.filters.pop(_id) if pop else self.filters[_id]
        return {k: scope.get(k, template[k]) for k in template}

    def _update_scope_statements(self, scope_to_set: Dict) -> None:
        """Applies a set of scope arguments to all statements within the script.

        Args:
            scope_to_set (dict):
                A full set of scope arguments.
        """
        for s in self._statements_all.values():
            s.tag.scope(**scope_to_set)

    def _update_scope_script(self, _id: Any[int, str], **kwargs) -> Dict:
        """Returns a valid set of scope args from an ``_id`` and the scope kwargs.

        Uses template property from configuration if the ``_id`` provided does
        not yet exist in ``script.filters``.

        Args:
            _id (Any[int, str]):
                Integer or string value for scope _id.
            **kwargs:
                Arguments provided to ``script.filter()`` (e.g. 'include_kw',
                'excl_anchor', etc).

        """
        _id = _id or (len(self.filters) + 1)
        scope_to_update = (
            self._scope_from_id(_id=_id, pop=True)
            if _id in self.filters
            else self.sn.cfg.scopes
        )
        merged_with_latest_filter = {
            arg: filters.union(kwargs[arg]) for arg, filters in scope_to_update.items()
        }
        self.filters[_id] = {k: v for k, v in merged_with_latest_filter.items() if v}
        return self.filters[_id]

    # DOCSTRING
    def _update_scope(self, as_id: Any[int, str], from_id: Any[int, str], **kwargs):
        _id = from_id or as_id
        if from_id:
            scope_config = self._scope_from_id(_id=_id, pop=False)
        else:
            scope_config = self.sn.cfg.scopes_from_kwargs(**kwargs)
        latest_scope = self._update_scope_script(_id=_id, **scope_config)
        self._update_scope_statements(scope_to_set=latest_scope)

    # DOCSTRING
    @contextmanager
    def filter(
        self,
        as_id: Any[str, int] = None,
        from_id: Any[str, int] = None,
        incl_kw: List = None,
        incl_obj: List = None,
        incl_desc: List = None,
        incl_anchor: List = None,
        incl_nm: List = None,
        excl_kw: List = None,
        excl_obj: List = None,
        excl_desc: List = None,
        excl_anchor: List = None,
        excl_nm: List = None,
        last: bool = False,
    ) -> ContextManager[Script]:
        # fmt: off
        if from_id and as_id:
            raise ValueError(
                f"script.filter() cannot accept `from_id` and `as_id` arguments"
                f" simultaneously."
            )
        if from_id and from_id not in self.filters:
            raise ValueError(
                f"from_id='{from_id}' does not exist in script.filters;"
                f"IDs that do exist are: {list(self.filters.keys())}"
            )
        # fmt: on
        try:
            if last:
                from_id, as_id = self._latest_scope_id, None
            self._update_scope(
                as_id=as_id,
                from_id=from_id,
                incl_kw=incl_kw,
                incl_obj=incl_obj,
                incl_desc=incl_desc,
                incl_anchor=incl_anchor,
                incl_nm=incl_nm,
                excl_kw=excl_kw,
                excl_obj=excl_obj,
                excl_desc=excl_desc,
                excl_anchor=excl_anchor,
                excl_nm=excl_nm,
                last=last,
            )
            self.filtered = True
            yield self
        except ValueError:
            raise
        finally:
            self.filtered = False
            self.reset()
            return self

    def _depth(self, full: bool = False) -> int:
        return len(self.statements) if not full else len(self._adjusted_contents)

    @property
    def depth(self) -> int:
        """Count of statements in the script."""
        return self._depth()

    @property
    def lines(self) -> int:
        """Number of lines in the script"""
        return sum(s.lines for s in self.statements.values())

    def _id(self, _id: Union[int, str]) -> int:
        """Returns index position of a statement given its index or tag name."""
        if isinstance(_id, int):
            return _id if _id > 0 else self.depth + _id + 1
        try:
            s = (
                self.contents(by_index=False)
                if _id in self.duplicates
                else self.contents(by_index=False, validate=False)
            )
            return s[_id].index
        except Exception as e:
            raise e

    @property
    def statements(self) -> Dict[int, Statement]:
        """All statements by index position included in the current context."""
        if not self.filtered:
            return self._statements_all
        statements = {s.index: s for s in self._statements_all.values() if s}
        return {
            current_idx: statements[prior_idx].index_to(current_idx)
            for current_idx, prior_idx in enumerate(sorted(statements), start=1)
        }

    @property
    def excluded(self):
        """All statements by index position excluded from the current context."""
        return {
            i: s for i, s in self._statements_all.items() if i not in self.statements
        }

    @property
    def executed(self) -> Dict[int, Statement]:
        """Executed statements by index position included in the current context."""
        return {i: s for i, s in self.statements.items() if s.executed}

    def statement(self, _id: Union[str, int] = None) -> Any[Statement, Empty, Diff]:
        """Fetch a single statement by _id."""
        index_of_id = self._id(_id=_id)
        return self.statements[index_of_id]

    def reset(self) -> None:
        """Resets indices and scope on all statements to their state as read from source.

        Invoked before exiting :meth:`filter()` context manger to reverse
        the revised indices set by :meth:`index_to()` and inclusion/
        exclusion scope set by :meth:`Statement.Tag.scope()`.

        """
        re_indexed = {s.reset() for s in self._statements_all.values()}
        by_index = {s.index: s for s in re_indexed}
        self._statements_all = {i: by_index[i] for i in sorted(by_index)}

    @property
    def duplicates(self) -> Dict[str, int]:
        """Dictionary of indistinct statement names/tags within script."""
        counted = collections.Counter([s.tag.nm for s in self._statements_all.values()])
        return {tag: cnt for tag, cnt in counted.items() if cnt > 1}

    def _validate_distinct_tags(
        self, statements_to_validate: Dict[int, Any[Statement, Marker]]
    ) -> Tuple[bool, str]:
        """validates statement tags are unique if contents are requested by
        statement/tag name as opposed to index position."""
        to_validate = statements_to_validate
        return (
            (
                len({s for s in to_validate})
                == len({s.name for s in to_validate.values()})
            ),
            f"Statement names in within {self.path.name} must be unique if "
            f"passing `by_index=False` to 'script.contents()'.\n"
            f"See 'script.duplicates' for a dictionary of the indistinct tag "
            f"names found within script.",
        )

    def contents(
        self,
        by_index: bool = True,
        ignore_scope: bool = False,
        markers: bool = False,
        validate: bool = True,
    ) -> Dict[Union[int, str], Statement]:
        """Dictionary of all executed statements with option to ignore current
        scope."""
        if not markers and ignore_scope:
            contents_to_return = self.statements
        elif not markers:
            contents_to_return = self._statements_all
        else:
            contents_to_return = self._adjusted_contents
        if by_index:
            return contents_to_return
        # validation to ensure keys are unique if fetching contents by tag name
        tags_are_unique, error_msg = self._validate_distinct_tags(contents_to_return)
        if validate and not tags_are_unique:
            raise Exception(error_msg)
        return {s.name: s for i, s in contents_to_return.items()}

    def dtl(self, full: bool = False) -> None:
        """Prints summary of statements within the current scope to console."""
        self._console.display()
        dtl = self.statements if not full else self._adjusted_contents
        depth = self._depth(full=full)
        for i, s in dtl.items():
            print(f"{str(i).rjust(len(str(depth)), ' ')}: {s}")

    def first_s(self):
        """First statement by index position."""
        return self.statements[min(self.statements)]

    def last_s(self):
        """Last statement by index position"""
        return self.statements[max(self.statements)]

    @property
    def first(self) -> Union[Statement, Empty, Diff]:
        """First statement executed."""
        by_start = {v.start_time: v for v in self.executed.values()}
        return by_start[min(by_start)]

    @property
    def last(self) -> Union[Statement, Empty, Diff]:
        """Last statement executed."""
        by_start = {v.start_time: v for v in self.executed.values()}
        return by_start[max(by_start)]

    def doc(
        self,
        alt_file_nm: str = None,
        alt_file_prefix: Optional[str] = None,
        alt_file_suffix: Optional[str] = None,
        incl_markers: Optional[bool] = True,
        incl_sql: Optional[bool] = True,
        sql_incl_export_disclaimer: Optional[bool] = True,
    ) -> Doc:
        """Doc object based on current context."""
        return Doc(
            sn=self.sn,
            path=self.path,
            contents=self._adjusted_contents,
            alt_file_nm=alt_file_nm,
            alt_file_prefix=alt_file_prefix,
            alt_file_suffix=alt_file_suffix,
            incl_sql=incl_sql,
            incl_markers=incl_markers,
            sql_incl_export_disclaimer=sql_incl_export_disclaimer,
        )

    @property
    def _intra_statement_markers(self):
        """All markers (raw text) above/between statements by index position."""
        return {
            i: self.intra_statement_marker_hashmap_txt[h]
            for h, i in self.intra_statement_marker_hashmap_idx.items()
        }

    @property
    def _trailing_statement_markers(self):
        """All markers (raw text) after the last statement by index position."""
        markers_r_unadjusted = {
            m
            for h, m in self.all_marker_hashmap.items()
            if not self.intra_statement_marker_hashmap_idx.get(h)
        }
        return {
            (self.depth + 1 + (i / 10)): b
            for i, b in enumerate(markers_r_unadjusted, start=1)
        }

    @property
    def _ordered_markers(self):
        """All markers (raw text), ordered by index position."""
        all_markers = {
            **self._intra_statement_markers,
            **self._trailing_statement_markers,
        }
        return {i: all_markers[i] for i in sorted(all_markers)}

    @property
    def _parsed_markers(self):
        """All markers (as dictionaries), ordered by index position."""
        return {
            i: self.sn.cfg.script.parse_marker(attrs_raw=block)
            for i, block in self._ordered_markers.items()
        }

    def _merge_markers(self):
        """Merges parsed markers/attributes with presets in ``snowmobile.toml``."""
        self.markers = self.sn.cfg.script.markdown.attrs.merge_markers(
            parsed_markers=self._parsed_markers
        )

    @property
    def _marker_counter(self):
        """Dictionary of the number of markers at each statement index."""
        return collections.Counter(round(k) for k in self.markers)

    def _get_marker_adjusted_idx(
        self, idx: int, counter: Counter, is_marker: bool = False, as_int: bool = False
    ) -> int:
        """Generates an index (int) taking into account statements and markers."""
        index = idx + (
            sum(v for k, v in counter.items() if k <= idx)
            if not is_marker
            else sum(1 for k in self.markers.keys() if k < idx)
        )
        return index if not as_int else round(index)
        # index = idx + (
        #     sum([v for k, v in counter.items() if k <= idx]) if not is_marker
        #     else sum([1 for k in self.markers.keys() if k < idx])
        # )

    def _adjusted_statements(self, counter: Counter):
        """Statements by adjusted index position."""
        return {
            self._get_marker_adjusted_idx(idx=i, counter=counter): s
            for i, s in self.statements.items()
        }

    def _adjusted_markers(self, counter: Counter):
        """Markers by adjusted index position."""
        adjusted_markers = {}
        for i, m in self.markers.items():
            i_adj = self._get_marker_adjusted_idx(
                idx=i, counter=counter, is_marker=True, as_int=True
            )
            adjusted_markers[i_adj] = m
        return adjusted_markers

    @property
    def _adjusted_contents(self):
        """All statements and markers by adjusted index position."""
        try:
            counter = Counter(round(k) for k in self.markers)
            adjusted_statements = self._adjusted_statements(counter=counter)
            adjusted_markers = self._adjusted_markers(counter=counter)
            contents = {**adjusted_markers, **adjusted_statements}
            return {i: contents[i] for i in sorted(contents)}
        except Exception as e:
            raise e

    def ids_from_iterable(self, _id: Union[Tuple, List],) -> List[int]:
        """Utility function to get a list of statement IDs given an `_id`.

        Invoked within script.run() if the `_id` parameter is either a:
            (1) tuple of integers (lower and upper bound of statement indices
                to run)
            (2) list of integers or strings (statement names or indices to run)
            (3) default=None; returns all statement indices within scope if so

        Args:
            _id Union[Tuple, List]:
                _id field provided to script.run() if it's neither an integer
                or a string.

        Returns:
            List[int]:
                A list of statement indices to run.

        """
        if isinstance(_id, List):
            return _id
        elif isinstance(_id, Tuple):
            start_intl, stop_intl = _id
            start, stop = (start_intl or 1), (self._id(_id=stop_intl) + 1)
            return [i for i in range(start, stop)]
        else:
            return list(self.statements)

    def _run(
        self,
        _id: Union[str, int] = None,
        results: bool = True,
        lower: bool = True,
        render: bool = False,
        **kwargs,
    ) -> None:
        """Runs a single statement given an `_id`.

        Args:
            _id (Union[str, int]):
                `_id` of the Statement to run (index position or statement
                name); default=`None` which will return all statement `_id`s
                within the current scope.
            results (bool):
                Return results from executed statement; default=`True`.
            lower (bool):
                Lower case column-names if results are returned; default=`True`.
            render (bool):
                Render the sql executed in (notebook-specific); default=`True`.

        """
        s = self.statement(_id=_id)
        try:
            s.run(
                results=results, lower=lower, render=render, **kwargs,
            )
        except Exception as e:
            raise e
        self._console.status(s)

    # DOCSTRING
    # TODO: Add an 'on_error' argument to control how exceptions are thrown if
    #   encountered.
    def run(
        self,
        _id: Union[str, int, Tuple, List] = None,
        results: bool = True,
        lower: bool = True,
        render: bool = False,
        silence_qa: bool = False,
        r: bool = False,
        **kwargs,
    ):
        if r:
            self.read()

        if isinstance(_id, (int, str)):
            self._run(
                _id=_id,
                results=results,
                lower=lower,
                render=render,
                silence_qa=silence_qa,
                **kwargs,
            )

        else:
            indices_to_execute = self.ids_from_iterable(_id=_id)
            self._console.display()
            for i in indices_to_execute:
                self._run(
                    _id=i,
                    results=results,
                    lower=lower,
                    render=render,
                    silence_qa=silence_qa,
                    **kwargs,
                )

    @property
    def _console(self):
        """External stdout object for console feedback without cluttering code."""
        self._stdout.statements = self.statements
        return self._stdout

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __str__(self) -> str:
        return f"snowmobile.Script('{self.name}')"

    def __repr__(self) -> str:
        return f"snowmobile.Script('{self.name}')"
