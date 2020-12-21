"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

import re
import time
from contextlib import contextmanager
from typing import Any, ContextManager, Dict, List, Set, Tuple, Union

import pandas as pd
import sqlparse
from IPython.core.display import Markdown, display
from snowflake.connector.errors import ProgrammingError

from snowmobile.core.configuration import configuration as cfg
from snowmobile.core.configuration import schema as config
from snowmobile.core.connector import Connector
from snowmobile.core.markup.section import Section


class Scope:
    """Handles the scope/context for :class:`Statement` objects and derived classes.

    Should never be interacted with from the user-facing API.

    Attributes:
        base (str):
            The left-most word within a statement tag. For **generic**
            statements this will be the `keyword` and for **QA** statements
            this will be the literal word ``qa``.
        component (str):
            The component within a given tag that is being evaluated; this will
            be exactly **one** of `kw`, `obj`, `anchor`, `desc`, or `nm`.
        incl_arg (str):
            The keyword argument that would be used to exclude a given
            component;
                *   e.g. if :attr:`component` is `kw`, :attr:`incl_arg` would
                    be ``incl_kw``.
        excl_arg (str):
            The keyword argument that would be used to exclude a given
            component; this would be the same as the above example except
            the value would be ``excl_kw`` as opposed to ``incl_kw``.
        fallback_to (dict):
            The default values to fall back to for :attr:`incl_arg` and
            :attr:`excl_arg` if they are not passed as a keyword argument
            by the user in :class:`Script`; defaults to including the
            :attr:`base` and excluding an empty list.
        provided_args (dict):
            The set of keyword arguments provided at the time of the last call
            to :meth:`eval()`.
        check_against_args (dict):
            The set of keyword arguments checked against at the time of the
            last call to :meth:`eval()`; will use provided arguments if they
            exist and the arguments from :attr:`fallback_to` otherwise.
        is_included (bool):
            Tag is included based on the results of the last call to
            :meth:`eval()`.
        is_excluded (bool):
            Tag is excluded based on the results of the last call to
            :meth:`eval()`.
        included (bool):
            Inclusion indicator for the tag as a whole; evaluates to `True`
            if the tag is included and not excluded as of the last call to
            :meth:`eval()`.

    """

    def __init__(
        self, base: str, arg: str,
    ):
        """Instantiates a :class:`Scope` object."""
        self.base = base.lower()  # 'qa'
        self.component: str = arg  # 'kw'
        self.incl_arg = f"incl_{arg}"  # 'incl_kw'
        self.excl_arg = f"excl_{arg}"  # 'excl_kw'
        self.fallback_to: Dict = {self.incl_arg: [base], self.excl_arg: list()}
        self.provided_args: Dict = dict()
        self.check_against_args: Dict = dict()
        self.is_included: bool = bool()
        self.is_excluded: bool = bool()
        self.included: bool = bool()

    def parse_kwargs(self, **kwargs) -> None:
        """Parses all filter arguments looking for those that match its base.

        Looks for include/exclude arguments within kwargs, populating
        :attr:`provided_args` with those that were provided and populates
        :attr:`check_against_args` with the same values if they were provided
        and fills in defaults from :attr:`fallback_to` otherwise.

        Args:
            **kwargs:
                Keyword arguments passed to :class:`Script.filter()` (e.g.
                `incl_kw`, `excl_kw`, ..)
        """
        self.provided_args = {
            k: v for k, v in kwargs.items() if k in [self.incl_arg, self.excl_arg]
        }
        self.check_against_args = {
            k: (self.provided_args.get(k) or self.fallback_to[k])
            for k in [self.incl_arg, self.excl_arg]
        }

    def matches_patterns(self, arg: str) -> bool:
        """Returns indication of if :attr:`base` matches a given set of patterns.

        Args:
            arg (str):
                Will either be the value of :attr:`incl_arg` or
                :attr:`exclude_arg`.

        Returns (bool):
            Indication of whether any matches were found.

        """
        escaped = any(
            re.findall(pattern=re.escape(self.base), string=p)
            for p in self.check_against_args[arg]
        )
        unescaped = any(
            re.findall(string=self.base, pattern=p)
            for p in self.check_against_args[arg]
        )
        return any([escaped, unescaped])

    def eval(self, **kwargs) -> bool:
        """Evaluates filter arguments and updates context accordingly.

        Updates the values of :attr:`is_included`, :attr:`is_excluded`, and
        :attr:`included`.

        Args:
            **kwargs:
                Keyword arguments passed to :class:`Script.filter()` (e.g.
                `incl_kw`, `excl_kw`, ..)

        Returns (bool):
            Indicator of whether or not the statement should be
            included/excluded based on the context/keyword arguments provided.

        """
        self.parse_kwargs(**kwargs)
        self.is_included = self.matches_patterns(arg=self.incl_arg)
        self.is_excluded = self.matches_patterns(arg=self.excl_arg)
        self.included = self.is_included and not self.is_excluded
        return self.included

    def __str__(self) -> str:
        return f"tag.Scope(base='{self.base}', arg='{self.component}')"

    def __repr__(self) -> str:
        return f"tag.Scope(base='{self.base}', arg='{self.component}')"

    def __bool__(self) -> bool:
        """Mirrors the state of :attr:`included`."""
        return self.included


class Tag:
    """Handles the decomposition/parsing of statement tags.

    Should never be instantiated directly by the user-facing API but its
    attributes are likely to be accessed often as part of :class:`Statement`
    and derived classes.

    Attributes:
        cfg (snowmobile.Configuration):
            :class:`snowmobile.Configuration` object; represents fully parsed
            **snowmobile.toml** file.
        patt (snowmobile.Schema.Pattern):
            :class:`snowmobile.Schema.Pattern` object; represents
            ``script.patterns`` section of **snowmobile.toml**.
        nm_pr (str):
            Provided tag name for a given :class:`Statement`; can be empty.
        index (int):
            Statement index position within :class:`Script`; can be empty.
        is_included (bool):
            Indicator of whether or not the combination of all scopes for this
            statement tag is included within a given context.
        incl_idx_in_desc (bool):
            Indicator of whether or not to include the statement index in the
            `description` component of the tag; defaults to `True` so that all
            generated statement tags are guaranteed to be unique for a given
            script.
                *   Mainly included for testing purposes where setting to
                    `False` enables comparing generated to provided statement
                    tags without having to change the index position of the
                    hard-coded/provided statement tag when adding/removing tests.
        part_keyword (tuple):
            A straight partition of the provided tag name on the
            ``keyword-delimiter`` specified in **snowmobile.toml**.
        is_struct_anchor (bool):
            Indicator of whether or :attr:`part_keyword` results in a tuple
            containing three items (e.g. if the statement tag is structured
            following the `keyword-object~description` taxonomy).
        kw_pr (str):
            The first item within :attr:`part_keyword` if :attr:`is_struct_anchor`
            evaluates to `True`; empty string otherwise.
        part_description (tuple):
            A straight partition of the last item in :attr:`part_keyword` on
            the ``name-delimiter`` specified in **snowmobile.toml**, assuming
            :attr:`is_struct_anchor` evaluates to `True`; empty string otherwise.
                *   In properly structure tags, the string being partitioned
                    is the `obj~description` portion of
                    `keyword-object~description`.
        is_struct_desc (bool):
            Indicator of whether or not :attr:`part_description` results in a
            tuple containing three items (e.g. if the remainder of the
            statement tag outside of the keyword follows the pre-determined
            taxonomy).
        obj_pr (str):
            The statement's `object name` if :attr:`is_struct_desc` evaluates
            to `True`; empty string otherwise.
        desc_pr (str):
            The statement's `description` if :attr:`is_struct_desc` evaluates
            to `True`; empty string otherwise.
        anchor_pr (str):
            The statement's `anchor`.
        first_line (str):
            A raw string of the first line of sql associated with the statement.
        incl_if_exists (bool):
            Indicator of whether or not :attr:`first_line` contains the term
            `if exists`; this is used for parsing purposes in the guts of the
            class.
        first_keyword (str):
            The first keyword found by sqlparse.Statement object; this can be
            multiple literal words in some cases (e.g. 'create table' as opposed
            to just 'create').
        first_line_remainder (str):
            The remainder of the first line once excluding the
            :attr:`first_keyword` and stripping repeating whitespace.
        kw (str):
            The final statement's **keyword** that is used elsewhere; this will
            be the provided keyword if a statement tag exists and a
            parsed/generated keyword otherwise.
        nm (str):
            The final statement's **name** that is used elsewhere; this will
            be the full tag name if a statement tag exists and a
            parsed/generated tag name otherwise.
        obj (str):
            The final statement's **object** that is used elsewhere; this will
            be the object within a tag if a statement tag exists and follows
            the correct structure and a parsed/generated object otherwise.
        desc (str):
            The final statement's **description** that is used elsewhere; this
            will be the description within a tag if a statement tag exists
            and follows the correct structure and a parsed/generated
            description otherwise.
        anchor (str):
            The final statement's **anchor** that is used elsewhere; this will
            be the anchor within a tag if a statement tag exists and follows
            the correct structure and a parsed/generated tag name otherwise.
        scopes (set[Scope]):
            Combination of all scopes for a given tag; this is essentially the
            all possible combinations of including/excluding any of the `kw`,
            `nm`, `obj`, `desc`, and `anchor` for a given instance of :class:`Tag`.

    """

    def __init__(
        self,
        configuration: cfg.Configuration,
        nm_pr: str = None,
        first_keyword: str = None,
        sql: str = None,
        index: int = None,
    ):
        self.cfg: cfg.Configuration = configuration
        self.patt: config.Pattern = self.cfg.script.patterns
        self.nm_pr = nm_pr or str()
        self.index = index or int()
        self.is_included: bool = True
        self.incl_idx_in_desc: bool = True

        self.part_keyword = self.nm_pr.partition(self.patt.core.sep_keyword)
        self.is_struct_anchor = len(self.part_keyword) == 3

        self.kw_pr = self.part_keyword[0] if self.is_struct_anchor else str()
        remainder = self.part_keyword[2] if self.is_struct_anchor else str()

        self.part_description = remainder.partition(self.patt.core.sep_desc)
        self.is_struct_desc = len(self.part_description) == 3

        self.obj_pr = self.part_description[0] if self.is_struct_desc else str()
        self.desc_pr = self.part_description[2] if self.is_struct_desc else str()

        self.anchor_pr = f"{self.kw_pr}{self.patt.core.sep_keyword}{self.obj_pr}"

        # ---------------------------------------------------------------------
        self.first_line = (sql or str()).split("\n")[0].lower().strip()
        self.incl_if_exists = "if exists" in self.first_line
        self.first_keyword = first_keyword or str()
        self.first_line_remainder = self.first_line_sans_keyword(
            self.first_line, self.first_keyword
        )

        # ---------------------------------------------------------------------
        self.kw = self.kw_pr or self.kw_ge
        self.nm = self.nm_pr or self.nm_ge
        self.obj = self.obj_pr or self.obj_ge
        self.desc = self.desc_pr or self.desc_ge
        self.anchor = self.anchor_pr or self.anchor_ge

        self.scopes: Set[Scope] = {Scope(**kwargs) for kwargs in self.scope_defaults}

    def scope(self, **kwargs) -> bool:
        """Evaluates all component's of a tag's scope against a set of filter args.

            **kwargs:
                Keyword arguments passed to :class:`Script.filter()` (e.g.
                `incl_kw`, `excl_kw`, ..)

        Returns (bool):
            Value indicating whether or not the statement should be included
            based on the outcome of the evaluation of all of its components.

        """
        self.is_included = all(s.eval(**kwargs) for s in self.scopes)
        return self.is_included

    @staticmethod
    def first_line_sans_keyword(first_line: str, first_keyword: str) -> str:
        """Returns the remainder of the first line of sql without its keyword."""
        part_first_line = first_line.partition(first_keyword)
        return " ".join([p.strip() for p in part_first_line if p][1:])

    def abs_first_keyword(self, first_keyword: str) -> str:
        """Returns the 'absolute' first keyword in the first line of sql.

        `Absolute` meaning a single word (e.g. if first word is 'create table',
        this will return 'create').

        Args:
            first_keyword (str):
                First keyword found by sqlparse.

        Returns (str):
            The `absolute` first keyword found within the first line of sql;
            if the keyword provided in ``first_keyword`` is only a single term
            to begin with, that value will be returned without any manipulation.

        """
        split_kw = first_keyword.split(" ")[0]
        return self.cfg.sql.kw_exceptions.get(split_kw, split_kw)

    @property
    def matched_terms(self) -> Dict[int, str]:
        """Searches the first line of sql for in-warehouse objects.

        Iterates through all values of ``script.patterns.named-objects``
        specified in **snowmobile.toml** and returns a dictionary of matches.

        Returns (dict[int, str]):
            A dictionary of matches by index position, 1 being the first match
            found; will return an empty dictionary of no matches are found.

        """
        numbered_terms = {i: t for i, t in enumerate(self.cfg.sql.named_objects)}
        matches = {
            i: re.findall(f"\\b{term}\\b", self.first_line)
            for i, term in numbered_terms.items()
        }
        return {i: numbered_terms[i] for i, v in matches.items() if v}

    def named_obj_in_line(self) -> str:
        """Returns the matched term if one is found, 'unknown' otherwise."""
        if self.matched_terms:
            return self.matched_terms[min(self.matched_terms)]
        else:
            return self.cfg.DEF_OBJ

    def description(self, named_obj: str):
        """Generates a description based on a named object.

        First checks to see if the `named_obj` provided is the fallback
        ('unknown'); if so it will return the default description of
        'statement', otherwise it will continue parsing the rest of the line.

        Args:
            named_obj (str):
                Named object found within the first line, returned from
                :meth:`named_obj_in_line()`.

        Returns (str):
            A string value to use for the description.

        """
        # fmt: off
        if named_obj == self.cfg.DEF_OBJ:
            idx_str = f" #{self.index}" if self.incl_idx_in_desc else str()
            return f"{self.cfg.DEF_DESC}{idx_str}"

        partitioned = [p for p in self.first_line_remainder.partition(named_obj) if p]
        if len(partitioned) < 2:
            return str()

        partitioned_rhs = [p for p in partitioned[-1].split(" ") if p]
        idx_to_use = -1 if self.incl_if_exists else 0

        return partitioned_rhs[idx_to_use]
        # fmt: on

    @property
    def generic_anchor_ge(self) -> Union[str, None]:
        """Returns the generic anchor for a keyword if matches a generic.

        Checks the parsed keyword against the generic anchors specified in
        ``script.patterns.generic-anchors`` within **snowmobile.toml**.

        Returns (Union[str, None]):
            The associated anchor as a string if a match exists; otherwise None.

        """
        return self.cfg.sql.generic_anchors.get(self.kw_ge)

    def generate_anchor(self, named_obj: str) -> str:
        """Generates an anchor based on a named object.

        Checks to see if the `named_obj` matches the fallback value of
        'unknown' **and** if the keyword parsed matches any generic anchors
        specified in **snowmobile.toml**; will return the generic anchor
        if so, otherwise a valid statement anchor based on the parsed
        keyword and the non-fallback named object provided.

        Args:
            named_obj (str):
                Named object found in first line of sql.

        Returns (str):
            Anchor component of the statement tag.

        """
        generic = self.generic_anchor_ge
        if named_obj == self.cfg.DEF_OBJ and generic:
            return generic
        else:
            return f"{self.kw_ge}-{named_obj}"

    @property
    def kw_ge(self):
        """Generated `keyword` for statement."""
        return self.abs_first_keyword(first_keyword=self.first_keyword)

    @property
    def obj_ge(self):
        """Generated `object` for statement."""
        return self.named_obj_in_line()

    @property
    def desc_ge(self):
        """Generated `description` for statement."""
        return self.description(named_obj=self.obj_ge)

    @property
    def anchor_ge(self):
        """Generated `anchor` for statement."""
        return self.generate_anchor(named_obj=self.obj_ge)

    @property
    def nm_ge(self):
        """Generated `name`/full statement tag for statement."""
        return f"{self.anchor_ge}{self.patt.core.sep_desc}{self.desc_ge}"

    @property
    def scope_defaults(self) -> List[Dict]:
        """Values of scope arguments from :class:`snowmobile.Configuration`
        that match attribute names from :class:`Tag`'s namespace.
        """
        return [{"base": vars(self)[k], "arg": k} for k in self.cfg.SCOPE_ATTRIBUTES]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __bool__(self) -> bool:
        return self.is_included

    def __str__(self) -> str:
        return f"statement.Tag(nm='{self.nm}')"

    def __repr__(self) -> str:
        return f"statement.Tag(nm='{self.nm}')"


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
    _OUTCOME_MAPPING: Dict[Any, Tuple] = {
        -2: ("-", "error"),
        -1: ("-", "skipped"),
        0: ("-", ""),
        1: ("warning", "failed"),
        2: ("info", "completed"),
        3: ("success", "passed"),
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
        self._outcome: bool = bool()

        self.sn = sn
        # self.statement: sqlparse.sql.Statement = sn.cfg.clean_parse(sql=statement)
        self.statement: sqlparse.sql.Statement = statement
        self.index: int = index or int()
        self.patterns: config.Pattern = sn.cfg.script.patterns
        self.results: pd.DataFrame = pd.DataFrame()

        self.outcome: int = int()
        self.outcome_txt: str = self._OUTCOME_MAPPING[self.outcome][1]
        self.outcome_html: str = str()

        self.start_time: int = int()
        self.end_time: int = int()
        self.execution_time: int = int()
        self.execution_time_txt: str = str()

        self.attrs_raw = attrs_raw
        self.is_tagged: bool = bool(self.attrs_raw)
        self.is_multiline: bool = "\n" in self.attrs_raw

        self.first_keyword = self.statement.token_first(skip_ws=True, skip_cm=True)
        self.sql = sn.cfg.script.isolate_sql(s=self.statement)

        self.tag: Tag = None
        self.attrs_parsed = self.parse()

    # @property
    # def index(self):
    #     return self.tag.index

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
        attrs = self.attrs_parsed
        for k, v in self.sn.cfg.script.markdown.attrs.from_namespace.items():
            attr = vars(self).get(k)
            if attr and k not in self._exclude_attrs:
                attrs[k] = attr
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
        sql_md = f"```sql\n{self.as_section().sql_md}\n```\n"
        display((Markdown(sql_md),))

    @property
    def name(self):
        """Quick access to tag name directly off the :class:`Statement`.."""
        return self.tag.nm

    @property
    def executed(self) -> bool:
        """Indicates whether the statement has been executed or not."""
        return self.outcome >= 1 or self.outcome == -2

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

    def reset(self) -> Statement:
        """Resets statement object to its original state as read from source.

        This includes:
            *   Resetting the statement's index to its original value.
            *   Resetting the statement *tag's* index to its original value.
            *   Resetting the :attr:`is_included` attribute of the statement's
                :attr:`tag` to `True`.

        """
        self.index = self._index
        self.tag.index = self._index
        self.tag.is_included = True
        return self

    @property
    def _outcome_latest(self):
        """Returns the numeric :attr:`outcome` value based on current context.


        ..note:
            *   The default value of :attr:`outcome` is 0.
            *   The first set of conditionals below will only modify its value
                if it's current value is still the default; if the statement
                encounters an error during execution, the value of :attr`outcome`
                will be changed to `-2` before exiting the context of
                :meth:`_run()` and the below codes will leave it as is.

        """
        if not self:  # statement is not included within the current context
            return -1
        elif not self.is_derived and not self.outcome:  # generic completed
            return 2
        elif not self.outcome:  # setting outcome for QA statements
            return 3 if self._outcome else 1
        else:  # keeping value of '-2' (i.e. error encountered)
            return self.outcome

    def update(self, **kwargs):
        """Updates outcome attributes and runs QA validation for derived classes.

        In total, updates are made to:
            *   :attr:`outcome`, assuming statement is within current scope.
            *   :attr:`outcome_txt', plain text form of outcome.
            *   :attr:`outcome_html`, outcome as an html admonition banner.

        Intended to be called directly after :meth:`process()`, which in the
        generic case will return the unmodified object but in derived classes,
        :meth:`process()` will perform validation on the results returned by
        the statement and alter the value of :attr:`_outcome`.

        """
        self.outcome = self._outcome_latest
        self.outcome_txt = self._OUTCOME_MAPPING[self.outcome][1]
        self.outcome_html = self._outcome_html(self.outcome_txt)
        self._validate_qa(**kwargs)

    def process(self):
        """Used by derived classes for validation logic of the returned results."""
        return self

    @contextmanager
    def _run(
        self, results: bool = True, lower: bool = True, render: bool = False, **kwargs,
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

        except ProgrammingError as e:
            self.outcome = -2
            raise e

        finally:
            if self and render:
                self.render()
            self.update(**kwargs)
            return self

    def run(
        self, results: bool = True, lower: bool = True, render: bool = False, **kwargs,
    ) -> Statement:
        with self._run(results=results, lower=lower, render=render, **kwargs) as r:
            return r.process()

    def _validate_qa(self, **kwargs):
        """Runs assertion based on the :attr:`_outcome` attribute set by QA classes."""
        if self.is_derived and not kwargs.get("silence_qa") and self:
            assert self._outcome, f"'{self.tag}' did not pass its QA check."

    @staticmethod
    def _validate_parsed(attrs_parsed: Dict):
        """Returns args to verify 'name' attribute is present in a multiline tag."""
        condition, msg = (
            attrs_parsed.get("name"),
            f"Required attribute 'name' not found in multi-line tag's "
            f"arguments;\n attributes found are: {','.join(list(attrs_parsed))}",
        )
        return condition, msg

    def _outcome_html(self, outcome_txt: str):
        """Utility to generation admonition html."""
        alert = self._OUTCOME_MAPPING[self.outcome][0]
        return f"""
<div class="alert-{alert}">
<center><b>====/ {outcome_txt} /====</b></center>
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
