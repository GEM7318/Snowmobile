"""
Module for post-processing attributes of ``snowmobile.Script`` in conjunction
with configuration options stored in *snowmobile.toml*.

These result in two files being exported into a `.snowmobile` folder in the
same directory as the .sql file that ``snowmobile.Script`` was instantiated
with.

Header-levels and formatting of tagged information is configured in the
*snowmobile.toml* file, with defaults resulting in the following structure::

        ```md

        # Script Name.sql         *[script name gets an 'h1' header]
        ----

        - **Tag1**: Value1         [tags are bolded, associated values are not]
        - **Tag2**: Value2         [same for all tags/attributes found]
        - ...

        **Description**           *[except for the 'Description' section]
                                  *[this is just a blank canvas of markdown..]
                                  *[..but this is configurable]

        ## (1) create-table~dummy_name *[statements get 'h2' level headers]
        ----

        - **Tag1**: Value1       *[tags can also be validations arguments..
        - **Arg1**: Val2          [that snowmobile will run on the sql results]

        **Description**          *[statements get one of these too]

        **SQL**                  *[their rendered sql does as well]
            ...sql
                ...
                ...
            ...


        ## (2) update-table~dummy_name2
        ----
        [structure repeats for all statements in the script]

        ```

"""
from __future__ import annotations

from typing import Dict, List, Union

import pandas as pd

from snowmobile.core.configuration import Configuration
from snowmobile.core.configuration import schema as cfg
from snowmobile.core.utils import parsing as p


# TESTS: Add tests for Name
class Name:
    """Handles attribute-name parsing including identification of wildcards.



    """

    def __init__(self, nm: str, config: Configuration):
        cfg_md = config.script.markdown
        cfg_script = config.script

        self.nm_raw = nm

        self.nm_stripped, self.flags = cfg_script.patterns.wildcards.partition_on_wc(
            attr_nm=nm
        )

        self.is_paragraph = cfg_script.patterns.wildcards.wc_paragraph in self.flags
        self.is_no_reformat = cfg_script.patterns.wildcards.wc_as_is in self.flags
        self.is_omit_nm = cfg_script.patterns.wildcards.wc_omit_attr_nm in self.flags

        self.is_results = self.check_reserved_nm(
            attr_name=self.nm_stripped,
            searching_for=cfg_md.attrs.reserved["query-results"].attr_nm,
        )
        self.is_sql = self.check_reserved_nm(
            attr_name=self.nm_stripped,
            searching_for=cfg_md.attrs.reserved["rendered-sql"].attr_nm,
        )

        if self.is_omit_nm:
            self.nm_adj = str()
            self.is_paragraph = True
        elif self.is_no_reformat:
            self.nm_adj = self.nm_stripped
        elif self.nm_stripped in cfg_md.attrs.from_namespace:
            self.nm_adj = cfg_md.attrs.from_namespace.get(self.nm_stripped)
        else:
            self.nm_adj = self.nm_stripped.title()

        self.specified_position = cfg_md.attrs.get_position(attr=self.nm_stripped)

    @staticmethod
    def check_reserved_nm(attr_name: str, searching_for: str) -> bool:
        """Safely checks for key terms within attribute names.

        Args:
            attr_name (str):
                Attribute name that we are checking (e.g. 'Results\\*')
            searching_for (str):
                Keyword we are searching for (e.g. 'results')

        """
        attr_name, searching_for = attr_name.lower(), searching_for.lower()
        len_attr, len_kw = len(attr_name), len(searching_for)
        if len_attr >= len_kw:
            return attr_name.startswith(searching_for)
        else:
            return False

    def __repr__(self):
        return f"Item.Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"

    def __str__(self):
        return f"Item.Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"


# TESTS: Add tests for Item
class Item(Name):
    """Represents a piece of text/content within a header section."""

    _DELIMITER = "~"
    _INDENT_CHAR = "\t"

    def __init__(
        self,
        index: int,
        flattened_attrs: tuple,
        config: Configuration,
        results: pd.DataFrame = None,
        sql_md: str = None,
    ):
        cfg_md = config.script.markdown
        self.is_first: bool = bool()

        self.cfg_md: cfg.Markdown = cfg_md
        self.index = index
        self.indent, nested, in_script_value = flattened_attrs

        self._split = nested.split(self._DELIMITER)

        super().__init__(nm=self._split[-1], config=config)

        self.depth = len(self._split) - 1
        self.indent: str = self._INDENT_CHAR * self.depth
        parent = self._split[self.depth - 1]
        self.parent = Name(nm=parent, config=config)

        self._is_reserved: bool = False
        if self.is_results:
            self.value = self.as_results(results=results, cfg_md=cfg_md)
            self._is_reserved = True
        elif self.is_sql:
            self.value = sql_md
            self._is_reserved = True
        else:
            self.value = in_script_value

    def is_sibling(self, other: Item) -> bool:
        return self.parent.nm_adj == other.parent.nm_adj

    def update(self, items: List[Item]):
        first_index_at_level = min({i.index for i in items if self.is_sibling(i)})
        if self.index == first_index_at_level and self.depth != 0:
            self.is_first = True
        return self

    @staticmethod
    def as_results(results: pd.DataFrame, cfg_md: cfg.Markdown):
        results_cfg = cfg_md.attrs.reserved["query-results"]

        display_record_limit = (
            cfg_md.result_limit if cfg_md.result_limit != -1 else results.shape[0]
        )
        results_sub = results.head(display_record_limit)
        if results_cfg.default_format == "markdown":
            return results_sub.to_markdown(showindex=False)
        else:
            return results_sub.to_html(index=False)

    @property
    def _as_md_parent(self):
        parent_indent = (self.depth - 1) * self._INDENT_CHAR
        return f"{parent_indent}{self.cfg_md.bullet_char} {self.parent.nm_adj}"

    @property
    def _as_md(self):
        attr_nm = self._format_attr(attr=self.nm_adj)
        attr_value = self._format_attr(attr=self.value, is_value=True)
        if not self.is_paragraph:
            return f"{self.indent}{self.cfg_md.bullet_char} {attr_nm}: {attr_value}"
        elif attr_nm:
            return f"\n{attr_nm}\n{attr_value}"
        else:
            return f"\n{attr_value}"

    def _format_attr(self, attr: str, is_value: bool = False):
        if self._is_reserved or self.is_no_reformat or self.is_paragraph:
            return attr
        wrap_character = (
            self.cfg_md.attr_nm_wrap_char
            if not is_value
            else self.cfg_md.attr_value_wrap_char
        )
        return f"{wrap_character}{attr}{wrap_character}"

    @property
    def md(self):
        if not self.is_first:
            return self._as_md
        else:
            return f"{self._as_md_parent}\n{self._as_md}"

    def __repr__(self):
        return f"section.Item('{self.nm_adj}')"

    def __str__(self):
        return f"section.Item('{self.nm_adj}')"


# TESTS: Add tests for Section
class Section:
    """Represents any (1-6 level) header section within `Script Name (doc).md`.


    This class is intended to be accessed as an attribute of
    `snowmobile.Script` and shouldn't need to be instantiated directly.

    In order to keep the core parsing functionality available without
    requiring execution of any statements in the script but also including
    execution data if available, the current implementation is heavily
    reliant on properties over attributes to reconcile what's populated in
    the `statements' and `executed` attributes of the `Script` object.



    Attributes:
        cfg_md (config.Markdown): Markdown configuration specified in the
            `snowmobile.toml` file.
        hx (str): String form of the markdown header tag (e.g. '#' for h1),
            based on the script/statement header-level specifications in
            `snowmobile.toml`.
        h_contents (str): Text to place in the header.
        index (int): The index position of the associated information, which
            indicates the statement number and is left as `None' for a script
            section.
        parsed (dict): Parsed arguments from within the sql script, returned
            from ``utils.parsing.parse_multiline()``.
        sql (str): Raw sql, will be `None` in the case of the top-level
            script-section if included.
        is_marker (bool): Indicating of whether the section metadata is
            script-level (as opposed to statement-level).

    """

    def __init__(
        self,
        config: Configuration,
        is_marker: bool = None,
        h_contents: str = None,
        index: int = None,
        parsed: Dict = None,
        sql: str = None,
        results: pd.DataFrame = None,
    ):
        """Instantiation of a ``script.Section`` object.

        Args:
            is_marker: Indicating of whether the section metadata is
                script-level (as opposed to statement-level).
            h_contents: Text to place in the header.
            index: The index position of the associated information,
                which indicates the statement number and is left as `None' for
                 a script section.
            parsed: Parsed arguments from within the sql script, returned
                from `utils.parsing.parse_multiline()`.
            sql: Raw sql, will be `None` in the case of the top-level
                script-section if included.

        """
        cfg_md = config.script.markdown
        self.cfg_md: cfg.Markdown = cfg_md
        self.is_marker = is_marker or bool()
        self.sql: str = sql
        self.results = results
        h_level = self.cfg_md.hx_marker if self.is_marker else self.cfg_md.hx_statement
        self.hx: str = int(h_level[1:]) * "#"
        self.h_contents: str = h_contents
        self.index: int = index
        grouped_attrs = self._group_attrs(attrs=parsed, groups=cfg_md.attrs.groups)
        self.parsed: Dict = self.reorder_attrs(parsed=grouped_attrs, config=config)
        self.items: List[Item] = self.parse_contents(
            sorted_parsed=self.parsed, config=config
        )

    def _add_reserved_attr(
        self,
        attrs: Dict[str, Union[str, Dict, bool]],
        cfg_md: cfg.Markdown,
        reserved_attr: str,
    ) -> Dict:
        """Adds reserved attributes based on configuration (i.e. SQL and Results).

        Args:
            attrs (Dict): Dictionary of currently parsed attributes.
            cfg_md (:class:`Markdown`): Markdown configuration object.
            reserved_attr (str): Name of reserved attribute.

        Returns (Dict):
            Dictionary with attribute added if 'include-by-default'=true in
            **snowmobile.toml**.

        """
        attr_config = cfg_md.attrs.reserved[reserved_attr]
        if not attr_config.include_by_default or self.is_marker:
            return attrs

        reserved_keyword = attr_config.attr_nm
        attrs_contain_results = [
            attr for attr in attrs if attr.lower().startswith(reserved_keyword)
        ]
        if not attrs_contain_results:
            attrs[attr_config.default_val] = attr_config.include_by_default
        return attrs

    @staticmethod
    def _group_attrs(attrs: Dict, groups: Dict) -> Dict:
        grouped = {}
        for parent, child_attrs in groups.items():
            children = {
                attr: attrs.pop(attr) for attr in child_attrs if attrs.get(attr)
            }
            if children:
                grouped[parent] = children
        return {**grouped, **attrs}

    def reorder_attrs(self, parsed: dict, config: Configuration) -> Dict:
        """Re-orders parsed attributes based on configuration."""
        cfg_md = config.script.markdown
        for reserved_attr_nm, reserved_attr in cfg_md.attrs.reserved.items():
            parsed = self._add_reserved_attr(
                attrs=parsed, cfg_md=cfg_md, reserved_attr=reserved_attr_nm,
            )
        included = {k: v for k, v in parsed.items() if cfg_md.attrs.include(attr=k)}
        specified_position_to_attr_nm: Dict[int, str] = {
            Name(nm=k, config=config).specified_position: k
            for k in included
            if Name(nm=k, config=config).specified_position
        }
        ordered_attr_nms = [
            specified_position_to_attr_nm[position]
            for position in sorted(specified_position_to_attr_nm)
        ]
        for attr_nm in ordered_attr_nms:
            parsed[attr_nm] = parsed.pop(attr_nm)
        return parsed

    def parse_contents(self, sorted_parsed: dict, config: Configuration) -> List[Item]:
        """Unpacks sorted dictionary of parsed attributes into formatted Items."""
        flattened = p.dict_flatten(
            attrs=sorted_parsed, bullet_char=config.script.markdown.bullet_char
        )
        items = [
            Item(
                index=i,
                flattened_attrs=v,
                config=config,
                results=self.results,
                sql_md=self.sql_md,
            )
            for i, v in enumerate(flattened, start=1)
        ]
        return [i.update(items=items) for i in items]

    @property
    def header(self) -> str:
        """Constructs the header for a section.

        Uses specifications in `snowmobile.toml` to determine:
            (1) The level of the header depending on whether it's a
                statement section or a script section.
            (2) Whether or not to include the statement index as part of the
                header.

        Returns:
            Formatted header line as a string.

        """
        if self.is_marker or not self.cfg_md.incl_index_in_sh:
            return f"{self.hx} {self.h_contents}"
        else:
            return f"{self.hx} ({self.index}) {self.h_contents}"

    @property
    def sql_md(self) -> str:
        """Returns renderable sql or an empty string if script-level section."""
        return f"```sql\n{self.sql.strip()};\n```" if not self.is_marker else ""

    @property
    def body(self):
        return "\n".join(i.md for i in self.items)

    @property
    def section(self) -> str:
        """Constructs a full section as a string from various components.

        Returns:
            Renderable string of the section.

        """
        return "\n".join([self.header, self.body])

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __repr__(self):
        return f"script.Section({str(vars(self))})"

    def __str__(self):
        return f"script.Section('{self.h_contents}')"
