"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

import re
from typing import Dict, Optional, Set, Union

from snowmobile.core.configuration import Configuration, Pattern

from .scope import Scope


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
        configuration: Configuration,
        nm_pr: Optional[str] = None,
        first_keyword: Optional[str] = None,
        sql: Optional[str] = None,
        index: Optional[int] = None,
    ):
        self.cfg: Configuration = configuration
        self.patt: Pattern = self.cfg.script.patterns
        self.nm_pr = nm_pr or str()
        self.index = index or int()
        self.is_included: bool = True
        self.incl_idx_in_desc: bool = True

        # ---------------------------------------------------------------------

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

        self.first_line = (sql or str()).strip("\n").split("\n")[0].lower().strip()
        self.incl_if_exists = "if exists" in self.first_line
        self.first_keyword = first_keyword or str()
        self.first_line_remainder = self.first_line_sans_keyword(
            first_line=self.first_line, first_keyword=self.first_keyword
        )

        # ---------------------------------------------------------------------

        self.kw = self.kw_pr or self.kw_ge
        self.nm = self.nm_pr or self.nm_ge
        self.obj = self.obj_pr or self.obj_ge
        self.desc = self.desc_pr or self.desc_ge
        self.anchor = self.anchor_pr or self.anchor_ge

        self.scopes: Set[Scope] = {
            Scope(**kwargs) for kwargs in self.cfg.scopes_from_tag(t=self)
        }

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
        # if len(partitioned) < 2:
        #     return str()

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
