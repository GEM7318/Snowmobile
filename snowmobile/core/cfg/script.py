"""
[script] section from **snowmobile.toml**, including subsections.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple, Union, Iterable, Optional

import sqlparse
from pydantic import Field

from snowmobile.core.utils import parsing as p
from snowmobile.core import errors

from .base import Base


class Wildcard(Base):
    """[script.patterns.wildcards]"""

    # fmt: off
    char_wc: str = Field(
        default_factory=str, alias="wildcard-character"
    )
    char_sep: str = Field(
        default_factory=str, alias="wildcard-delimiter"
    )
    wc_paragraph: str = Field(
        default_factory=str, alias="denotes-paragraph"
    )
    wc_as_is: str = Field(
        default_factory=str, alias="denotes-no-reformat"
    )
    wc_omit_attr_nm: str = Field(
        default_factory=str, alias="denotes-omit-name-in-output"
    )
    # fmt: on

    def find_first_wc_idx(self, attr_nm: str) -> int:
        """Finds index of the first unescaped wildcard in an attribute name.

        Args:
            attr_nm (str): Attribute name to search through.

        Returns (int):
            Index position of first unescaped wildcard or 0 if one does not exist.

        """
        idx = 0
        for i, c in enumerate(attr_nm):
            if c == self.char_wc and "\\" != attr_nm[i - 1]:
                idx = i
                break
        return idx

    def partition_on_wc(self, attr_nm: str) -> Tuple[str, List[str]]:
        """Parses attribute name into its display name and its wildcards.

        Uses :meth:`Wildcard.find_first_wc_idx()` to determine if **attr_nm**
        contains a valid wildcard.

        Args:
            attr_nm (str): Attribute name to parse.

        Returns (Tuple[str, List[str]]):
            Tuple containing the attribute display name and a list of its
            wildcards if present and an empty list otherwise.

        """
        idx_of_first_unescaped = self.find_first_wc_idx(attr_nm=attr_nm)
        has_valid_wc = idx_of_first_unescaped != 0

        wildcards = []
        if has_valid_wc:
            nm_to_strip = attr_nm[:idx_of_first_unescaped]
            wildcards = attr_nm[idx_of_first_unescaped:].split("_")
        else:
            nm_to_strip = attr_nm

        stripped_nm = nm_to_strip.replace(f"\\{self.char_wc}", self.char_wc)
        return stripped_nm, wildcards


class Reserved(Base):
    """[script.markdown.attributes.reserved]"""

    # fmt: off
    include_by_default: bool = Field(
        default_factory=bool, alias="include-by-default"
    )
    attr_nm: str = Field(
        default_factory=str, alias="attribute-name"
    )
    default_val: str = Field(
        default_factory=str, alias="default-to"
    )
    default_format: str = Field(
        default_factory=str, alias="format"
    )
    # fmt: on


class Marker(Base):
    """[script.markdown.attributes.markers]"""

    # fmt: off
    nm: str = Field(
        default_factory=str, alias="name"
    )
    group: str = Field(
        default_factory=str, alias="as-group"
    )
    attrs: Dict = Field(
        default_factory=dict, alias="attrs"
    )
    raw: str = Field(
        default_factory=int, alias="raw-text"
    )
    index: int = Field(
        default_factory=int, alias="index"
    )
    # fmt: on

    def __init__(self, **data):
        super().__init__(**data)
        if not self.attrs:
            self.attrs = {
                k: v for k, v in data.items() if k not in self.dict(by_alias=True)
            }

    def add(self, attrs: Dict) -> Marker:
        """Add to existing attributes."""
        for k, v in attrs.items():
            self.attrs[k] = v
        return self

    def split_attrs(self, attrs: Dict) -> Tuple[Dict, Dict]:
        """Splits attributes into user-defined-only and shared with snowmobile.toml.

        Args:
            attrs (Dict):
                Dictionary of parsed arguments.

        Returns (Tuple[Dict, Dict]):
            Tuple of (shared_with_snowmobile_toml_attrs, new_attrs)

        """
        shared = {k: v for k, v in attrs.items() if k in self.attrs}
        new = {k: attrs[k] for k, v in attrs.items() if k not in self.attrs}
        return shared, new

    def update(self, attrs: Dict) -> Marker:
        """Merges parsed attributes with configuration attributes"""
        self.raw = attrs.pop("raw-text")
        shared_attrs, new_attrs = self.split_attrs(attrs=attrs)
        self.attrs.update(shared_attrs)
        self.attrs = {self.group: self.attrs} if self.group else self.attrs
        self.add(attrs=new_attrs)
        return self

    def set_name(self, name: str, overwrite: bool = False) -> Marker:
        """Sets the name attribute."""
        if self.nm and not overwrite:
            return self
        self.nm = name.replace("_", "")
        return self

    def as_args(self):
        """Returns a dictionary of arguments for :class:`Section`."""
        if self.attrs.get("name"):
            self.nm = self.attrs.pop("name")
        if self.attrs.get("marker-name"):
            _ = self.attrs.pop("marker-name")
        return {"h_contents": self.nm, "parsed": self.attrs, "is_marker": True}

    def __str__(self):
        return f"Marker('{self.nm}')"

    def __repr__(self):
        return f"Marker('{self.nm}')"


class Attributes(Base):
    """[script.markdown.attributes]"""

    # fmt: off
    excluded: List[str] = Field(
        default_factory=list, alias='exclude'
    )
    from_namespace: Dict[str, str] = Field(
        default_factory=dict, alias='from-namespace'
    )
    groups: Dict = Field(
        default_factory=dict, alias="groups"
    )
    order: List[str] = Field(
        default_factory=list, alias="attribute-order"
    )
    reserved: Dict[str, Reserved] = Field(
        default_factory=dict, alias="reserved"
    )
    markers: Dict[str, Marker] = Field(
        default_factory=dict, alias="attribute-markers"
    )
    # fmt: on

    def __init__(self, **data):

        super().__init__(**data)

        self.order = data.get("order", dict()).get("attribute-order", list())

        for attr_nm, defaults in data["reserved"].items():
            args = {"attribute-name": attr_nm}
            self.reserved[attr_nm] = Reserved(**{**args, **defaults})

        # markers = data.get("markers")
        for marker, marker_attrs in data["markers"].items():
            self.markers[marker] = Marker(**marker_attrs).set_name(name=marker)

    def exclude(self, item: str):
        """Adds an item (argument name) to list of exclusions."""
        if item not in self.excluded:
            self.excluded.append(item)
        return self

    def get_marker(self, name: str):
        """Fetches a template marker from :attr:`markers`."""
        return self.markers.get(f"__{name}__")

    def merge_markers(self, parsed_markers: Dict[int, Dict]) -> Dict[int, Marker]:
        """Merges markers parsed from script with template markers in snowmobile.toml.

        Does the following:
            *   Consumes all parsed attributes from markers found in a script
            *   Tries to pull a pre-configured marker based on its time and
                updates its pre-configured values with those provided in the
                script if so
            *   If it doesn't find a pre-configured marker based on the marker
                name, it will instantiate a new marker instance from the
                arguments provided in the script.

        Args:
            parsed_markers (Dict[int, Dict]):
                All parsed raw marker arguments from a script by index position.

        Returns (Dict[int, Marker]):
            Instantiated markers for all attributes, merging those with
            matching names to pre-configured markers in snowmobile.toml.

        """
        total = {}
        for i, ms in parsed_markers.items():
            m = self.get_marker(name=ms["marker-name"])
            m = m.update(attrs=ms) if isinstance(m, Marker) else Marker(**ms)
            total[i] = m
        return total

    def get_position(self, attr: str) -> int:
        """Returns the position for an attribute based on snowmobile_ext.toml.

        Will return 0 if not included in order-by configuration.

        """
        attr = attr.lower()
        ordered = [w.lower() for w in self.order]
        if attr not in ordered:
            return int()
        for i, ordered_attr in enumerate(ordered, start=1):
            if attr == ordered_attr:
                return i

    def included(self, attrs: Dict) -> Dict:
        """Checks if an attribute has been marked for exclusion from render.
        """
        return {k: v for k, v in attrs.items() if k not in self.excluded}

    def group_parsed_attrs(self, parsed: Dict) -> Dict:
        """Nests attributes into dictionaries that are configured as groups.
        """
        grouped = {}
        attrs = self.included(parsed)
        for parent, child_attrs in self.groups.items():
            children = {
                attr: attrs.pop(attr) for attr in child_attrs if attrs.get(attr)
            }
            if children:
                grouped[parent] = children
        return {**grouped, **attrs}

    def _add_reserved(self, nm: str, attrs: Dict, is_marker: bool = False):
        """Adds a single reserved attr's configuration to attrs.

        Args:
            nm: Attribute name.
            attrs: Full dictionary of attributes.
            is_marker: Dictionary of attributes is for a marker.

        Returns: Revised attrs.

        """
        reserved_attr = self.reserved[nm]
        reserved_nm = reserved_attr.attr_nm
        if is_marker:
            return attrs
        if not attrs.get(reserved_nm) and reserved_attr.include_by_default:
            attrs[reserved_attr.default_val] = reserved_attr.include_by_default
        elif reserved_attr.include_by_default:
            attrs[reserved_attr.default_val] = attrs[reserved_nm]
        return attrs

    def add_reserved_attrs(self, attrs: Dict, is_marker: bool = False):
        """Batch modifies all reserved attributes to their configuration."""
        attrs = {k: v for k, v in attrs.items()}  # work on a copy of attrs
        for nm in self.reserved:
            attrs = self._add_reserved(nm=nm, attrs=attrs, is_marker=is_marker)
        return attrs


class Core(Base):
    """[script.patterns.core]"""

    # fmt: off
    to_open: str = Field(
        default_factory=str, alias='open-tag'
    )
    to_close: str = Field(
        default_factory=str, alias='close-tag'
    )
    sep_keyword: str = Field(
        default_factory=str, alias="keyword-delimiter"
    )
    sep_desc: str = Field(
        default_factory=str, alias="description-delimiter"
    )
    # fmt: on


class Markdown(Base):
    """[script.markdown]"""

    # fmt: off
    hx_marker: str = Field(
        default_factory=str, alias='default-marker-header'
    )
    hx_statement: str = Field(
        default_factory=str, alias='default-statement-header'
    )
    bullet_char: str = Field(
        default_factory=str, alias='default-bullet-character'
    )
    attr_nm_wrap_char: str = Field(
        default_factory=str, alias="wrap-attribute-names-with"
    )
    attr_value_wrap_char: str = Field(
        default_factory=str, alias="wrap-attribute-values-with"
    )
    incl_index_in_sh: bool = Field(
        default_factory=bool, alias='include-statement-index-in-header'
    )
    result_limit: int = Field(
        default_factory=int, alias="limit-query-results-to"
    )
    attrs: Attributes = Field(
        default_factory=Attributes, alias="attributes"
    )
    # fmt: on

    def pref_header(
        self, is_marker: bool = False, from_wc: Optional[str] = False
    ) -> str:
        """Creates header prefix based on specifications."""
        h_level = self.hx_marker if is_marker else self.hx_statement
        if not from_wc:
            return int(h_level.strip()[1:]) * "#"
        wc_only = "".join(c for c in from_wc if c == "*")
        return len(wc_only) * "#"


class Pattern(Base):
    """[script.patterns]"""

    # fmt: off
    core: Core = Field(
        default_factory=Core, alias="core"
    )
    wildcards: Wildcard = Field(
        default_factory=Wildcard, alias="wildcards"
    )
    # fmt: on


class Tolerance(Base):
    """[script.qa.default-tolerance]"""

    # fmt: off
    relative: float = Field(
        default_factory=float, alias="relative"
    )
    absolute: float = Field(
        default_factory=float, alias="absolute"
    )
    only_matching_rows: bool = Field(
        default_factory=bool, alias="only-compare-matching-rows"
    )
    # fmt: on


class QA(Base):
    """[script.qa]"""

    # fmt: off
    partition_on: str = Field(
        default_factory=str, alias="partition-on"
    )
    ignore_patterns: List = Field(
        default_factory=list, alias="ignore-patterns"
    )
    compare_patterns: List = Field(
        default_factory=list, alias="compare-patterns"
    )
    end_index_at: str = Field(
        default_factory=str, alias="end-index-at"
    )
    tolerance: Tolerance = Field(
        default_factory=Tolerance, alias="default-tolerance"
    )
    # fmt: on


class Type(Base):
    """snowmobile_ext.toml: [tag-to-type-xref]"""

    # fmt: off
    as_str: List = Field(
        default_factory=list, alias="string"
    )
    as_list: List = Field(
        default_factory=list, alias="list"
    )
    as_float: List = Field(
        default_factory=list, alias="float"
    )
    as_bool: List = Field(
        default_factory=list, alias="bool"
    )
    # fmt: on


class Script(Base):
    """[script]"""

    # fmt: off
    patterns: Pattern = Field(
        default_factory=Pattern, alias="patterns"
    )
    markdown: Markdown = Field(
        default_factory=Markdown, alias="markdown"
    )
    qa: QA = Field(
        default_factory=QA, alias="qa"
    )
    types: Type = Field(
        default_factory=Type, alias="tag-to-type-xref"
    )
    export_dir_nm: str = Field(
        default_factory=str, alias="export-dir-name"
    )
    # fmt: on

    @staticmethod
    def power_strip(val_to_strip: str, chars_to_strip: Iterable[str]) -> str:
        """Exhaustively strips a string of specified leading/trailing characters."""
        while any(val_to_strip.strip(c) != val_to_strip for c in chars_to_strip):
            for c in chars_to_strip:
                val_to_strip = val_to_strip.strip(c)
        return val_to_strip

    def arg_to_string(self, arg_as_str: str) -> str:
        """Strips an argument as a string down to its elemental form."""
        return self.power_strip(val_to_strip=arg_as_str, chars_to_strip=["'", '"', " "])

    def arg_to_list(self, arg_as_str: str) -> List[str]:
        """Converts a list as a string into a list."""
        return [
            self.power_strip(v, chars_to_strip=['"', "'", "[", "]", " "])
            for v in arg_as_str.split(",")
        ]

    def arg_to_float(self, arg_as_str: str) -> float:
        """Strips a string down to its elemental form and converts to a float."""
        return float(self.arg_to_string(arg_as_str))

    def arg_to_bool(self, arg_as_str: str) -> bool:
        """Converts a boolean in string-form into a boolean value."""
        str_replacements = {"true": True, "false": False}
        return str_replacements[self.arg_to_string(arg_as_str).lower()]

    def parse_arg(self, arg_key: str, arg_value: str):
        """Parses an argument into its target data type based on its `arg_key`
        and the ``script.tag-to-type-xref`` defined in **snowmobile.toml**."""
        arg_key, _, _ = arg_key.partition("*")
        if arg_key in self.types.as_list:
            return self.arg_to_list(arg_as_str=arg_value)
        elif arg_key in self.types.as_float:
            return self.arg_to_float(arg_as_str=arg_value)
        elif arg_key in self.types.as_bool:
            return self.arg_to_bool(arg_as_str=arg_value)
        else:
            return self.arg_to_string(arg_as_str=arg_value)

    @staticmethod
    def split_args(args_str: str) -> List[str]:
        """Returns a list of arguments based on splitting string on double
        underscores and stripping results."""
        matches = [s.strip() for s in re.split(r"\n*__", args_str)]
        return [s for s in matches if not s.isspace() and s]

    def parse_split_arguments(self, splitter: List[str]) -> Dict:
        """Returns a dictionary of argument-index to argument keys and values."""
        args_parsed = {}
        for i, s in enumerate(splitter, start=1):
            keyword, _, arg = s.partition(":")
            if keyword and arg:
                args_parsed[keyword.strip()] = self.parse_arg(
                    arg_key=keyword, arg_value=arg
                )
        return args_parsed

    def parse_str(
        self, block: str, strip_blanks: bool = False, strip_trailing: bool = False
    ) -> Dict:
        """Parses a string of statement tags/arguments into a valid dictionary.

        Args:
            block (str):
                Raw string of all text found between a given open/close tag.
            strip_blanks (bool):
                Strip blank lines from string; defaults to `False`.
            strip_trailing (bool):
                Strip trailing whitespace from the string; defaults to `False`.

        Returns (dict):
            Dictionary of arguments.

        """
        stripped = p.strip(block, blanks=strip_blanks, trailing=strip_trailing)
        splitter = self.split_args(args_str=stripped)
        return self.parse_split_arguments(splitter=splitter)

    def as_parsable(
        self,
        raw: str,
        is_multiline: Optional[bool] = None,
        is_marker: Optional[bool] = None,
        lines: Optional[int] = None,
    ) -> str:
        """Returns a raw string wrapped in open/close tags.

        Used for taking a raw string of marker or statement attributes and
        wrapping it in open/close tags before exporting, making the script
        being exported re-parsable by `snowmobile`.

        """
        raw = raw.strip("\n")
        _open = self.patterns.core.to_open
        _close = self.patterns.core.to_close
        if is_marker:
            lines = (0 if lines == -1 else lines or 1) * "\n"
            return f"{_open}\n{raw}\n{_close}{lines}"
        elif is_multiline:
            return f"{_open}\n{raw}\n{_close}"
        return f"{_open}{raw}{_close}"

    def find_spans(self, sql: str) -> Dict[int, Tuple[int, int]]:
        """Finds indices of script tags given a sql script as a string and an
        open and close pattern of the tags."""

        to_open, to_close = self.patterns.core.to_open, self.patterns.core.to_close
        _open, _close = re.compile(re.escape(to_open)), re.compile(re.escape(to_close))

        open_spans = {
            i: m.span()[1] for i, m in enumerate(re.finditer(_open, sql), start=1)
        }
        close_spans = {
            i: m.span()[0] for i, m in enumerate(re.finditer(_close, sql), start=1)
        }
        try:
            if len(open_spans) != len(close_spans):
                raise AssertionError(
                    f"parsing.find_tags() error.\n"
                    f"Found different number of open-tags to closing-tags; please check "
                    f"script to ensure each open-tag matching '{to_open}' has an "
                    f"associated closing-_tag matching '{to_close}'."
                )
            return {i: (open_spans[i], close_spans[i]) for i in close_spans}
        except AssertionError as e:
            raise e

    def find_tags(self, sql: str) -> Dict[int, str]:
        """Finds indices of script tags given a sql script as a string and an
        open and close pattern of the tags."""
        try:
            bounded_arg_spans_by_idx = self.find_spans(sql=sql)
            return {
                i: sql[span[0] : span[1]]
                for i, span in bounded_arg_spans_by_idx.items()
            }
        except AssertionError as e:
            raise e

    def find_block(self, sql: str, marker: str) -> str:
        """Finds a block of arguments based on a marker.

        Markers expected by default are the __script__ and __appendix__ markers.

        """
        tags = [t for t in self.find_tags(sql=sql).values() if marker in t]
        assert len(tags) <= 1, (
            f"Found more than one tag within script containing '{marker}'; "
            f"expected exactly one."
        )
        return tags[0] if tags else str()

    def has_tag(self, s: sqlparse.sql.Statement) -> bool:
        """Checks if a given statement has a tag that directly precedes the sql."""
        s_tot: str = s.token_first(skip_cm=False).value
        spans_by_index = self.find_spans(sql=s_tot)
        if not spans_by_index:
            return False

        _, last_span_close_idx = spans_by_index[max(spans_by_index)]
        s_remainder = s_tot[last_span_close_idx:]
        if not s_remainder.startswith(self.patterns.core.to_close):
            raise Exception(
                f"Last span identified in the below statement did not end with"
                f" the expected close-pattern of {self.patterns.core.to_close}"
                f"; see sql below.\n\n{s_tot}"
            )

        return len(s_remainder.split("\n")) == 2

    @staticmethod
    def is_marker(raw: str):
        """Checks if a raw string of arguments has a marker on the first line."""
        if not raw:
            return bool(raw)
        first_line = [v for v in raw.split("\n") if v][0]
        return bool(re.findall("__.*__", first_line))

    @staticmethod
    def is_valid_sql(s: sqlparse.sql.Statement) -> bool:
        """Verifies that a given sqlparse.sql.Statement contains valid sql."""
        has_sql = bool(s.token_first(skip_cm=True, skip_ws=True))
        return has_sql and not s.value.isspace()

    @staticmethod
    def isolate_sql(s: sqlparse.sql.Statement) -> str:
        """Isolates just the sql within a :class:`sqlparse.sql.Statement` object."""
        s_sql = s.token_first(skip_cm=True)
        if not s_sql:
            return str()
        first_keyword_idx = s.token_index(s_sql)
        sql = "".join(c.value for c in s[first_keyword_idx:])
        return sql.strip().strip(";")

    def split_sub_blocks(self, s: sqlparse.sql.Statement) -> Tuple[List, str]:
        """Breaks apart blocks of arguments within a :class:`sqlparse.sql.Statement`.

        Note:
            *   :meth:`sqlparse.parsestream()` returns a list of
                :class:`sqlparse.sql.Statement` objects, each of which includes
                all text (comments) between the last character of the prior
                statement and the first character of the current one.
            *   :meth:`split_sub_blocks()` traverses that space and identifies
                all spans of text wrapped in `open` (``/*-``) and `close`
                (``-*/``) tags, storing their index positions relative to the
                other statements & markers.
            *   These are stored as :class:`snowmobile.core.Script` attributes
                as statements are parsed and so that they can be exported in
                the appropriate order to a markdown file.

        Args:
            s (sqlparse.sql.Statement):
                :class:`sqlparse.sql.Statement` object.

        Returns (Tuple[List, str]):
            A tuple containing:
                1.  A list of __marker__ blocks if they exist; empty list otherwise
                2.  The last tag/block before the start of the actual SQL (e.g. the
                    tag/block that is associated with the statement passed to ``s``.

        """
        blocks = list(self.find_tags(sql=s.value).values())
        markers = [b for b in blocks if self.is_marker(raw=b)]
        is_tagged = self.has_tag(s=s)
        tag = blocks[-1] if is_tagged else str()
        return markers, tag

    def name_from_marker(self, raw: str) -> str:
        """Extracts a marker name (e.g. 'script' from within __script__)."""
        splitter = self.split_args(args_str=raw)
        if not splitter:
            raise Exception(
                f"snowmobile parsing error: parsing.name_from_marker() called on"
                f"an empty string."
            )
        return splitter[0]

    def parse_name(
        self, raw: str, offset: Optional[int] = None, silence: bool = False
    ) -> str:
        """Parses name from a raw set of arguments if not given an explicit tag."""
        by_line = raw.strip("\n").split("\n")
        offset = offset or 0
        if by_line[offset].startswith("__"):
            e = errors.InvalidTagsError(
                msg=f"""
invalid statement tags provided.
multi-line statement tags without an explicit `__name` attribute must include
a name not beginning with '__' on the first line within the open & closing tag;
first line found is:\n```\n{raw}\n```.
"""
            )
            if silence:
                return str()
            raise e
        return self.power_strip(by_line[offset], ['"', "'", " "])

    @staticmethod
    def add_name(nm_title: str, nm_marker: str, attrs: dict, overwrite: bool = False):
        """Adds a name to a set of parsed marker attributes.

        Accepts a name and a dict of parsed attributes from a marker and:
            1.  Checks to see if there's an explicit 'name' declared within the
                attributes
            2.  If not explicitely declared **or** explicitely declared and
                `overwrite=False`, it will add the `nm` value to the attributes as 'name'.
            3.  It will also add the 'nm' value to the attributes as 'marker-name'
                to be used by the :class:`Marker` when cross-referencing the
                __name__ with template markers in ``snowmobile.toml``.

        Args:
            nm_title (str):
                The name of the marker as either:
                    1.  Returned value from :meth:`name_from_marker()`
                    2.  Returned value from :meth:`parse_name()`
                    3.  None if neither is provided
            nm_marker (str):
                The string value wrapped in ``__`` on the first line of the
                argument block.
            attrs (dict):
                A dictionary of parsed attributes as returned from :func:`parse_str()`.
            overwrite (bool):
                Indicator of whether or not to overwrite a 'name' attribute declared
                within the .sql script.

        """
        attrs["marker-name"] = nm_marker
        if nm_title:
            attrs["name"] = nm_title
        if not nm_title or overwrite:
            attrs["name"] = nm_marker
        return attrs

    def parse_marker(self, attrs_raw: str) -> Dict:
        """Parses a raw string of __marker__ text between an open and a close pattern."""
        parsed = self.parse_str(attrs_raw)
        nm_title = parsed.get("name") or self.parse_name(
            raw=attrs_raw, offset=1, silence=True
        )
        marker_nm = self.name_from_marker(attrs_raw)
        self.add_name(
            nm_title=nm_title, nm_marker=marker_nm, attrs=parsed, overwrite=False
        )
        parsed["raw-text"] = attrs_raw
        return parsed

    @staticmethod
    def ensure_sqlparse(
        sql: Union[sqlparse.sql.Statement, str]
    ) -> sqlparse.sql.Statement:
        """Accepts a string or a sqlparse.sql.Statement and returns a sqlparse.sql.Statement.

        Necessary in order to accommodate the dynamic addition of statements as
        strings to an existing :class:`Script` object which will instantiate
        the new :class`Statement` objects from raw strings as opposed to from
        :class:`sqlparse.sql.Statement` objects as is the case when read from
        a source file.

        Args:
            sql (Union[sqlparse.sql.Statement, str]):
                Either a string of sql or an already parsed
                sqlparse.sql.Statement object.

        Returns (sqlparse.sql.Statement):
            A parsed sql statement.

        """
        if isinstance(sql, sqlparse.sql.Statement):
            return sql

        parsed = [
            s
            for s in sqlparse.parsestream(stream=sql.strip().strip(";"))
            if not s.value.isspace()
        ]
        assert (
            parsed
        ), f'sqlparse.parsestream("""\n{sql}"""\n) returned an empty statement.'
        return parsed[0]
