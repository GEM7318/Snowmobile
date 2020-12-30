"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

from typing import Optional, Set

from . import Snowmobile, Configuration, Scope
from .schema import Pattern


class Tag(Snowmobile):
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
            Indicator of whether or :attr:`part_keyword` as_df in a tuple
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
            Indicator of whether or not :attr:`part_description` as_df in a
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
        sql: Optional[str] = None,
        index: Optional[int] = None,
    ):
        super().__init__()

        # configuration
        # -------------
        self.cfg: Configuration = configuration
        self.patt: Pattern = self.cfg.script.patterns
        self.index = index or int()
        self.is_included: bool = True
        self.incl_idx_in_desc: bool = True

        # '_pr' placeholders
        # ------------------
        self.nm_pr = nm_pr or str()
        self.anchor_pr = str()
        self.kw_pr = str()
        self.obj_pr = str()
        self.desc_pr = str()

        # '_pr' parsing
        # -------------
        self.part_desc = tuple(
            v for v in self.nm_pr.partition(self.patt.core.sep_desc) if v
        )
        if len(self.part_desc) == 3:  # ('create table', '~', 'sample_records')
            anchor_vf = [  # ensure no extra space between words
                self.cfg.script.power_strip(v, " ")
                for v in self.part_desc[0].split(" ")
                if self.cfg.script.power_strip(v, " ")
            ]
            self.anchor_pr = " ".join(anchor_vf)  # 'create table'
            self.kw_pr = anchor_vf[0]             # 'create'
            self.obj_pr = (                       # 'table'
                " ".join(anchor_vf[1:]) if len(anchor_vf) > 2 else str()
            )
            self.desc_pr = " ".join(              # 'sample records'
                self.cfg.script.power_strip(v, " ")
                for v in self.part_desc[-1].split(" ")
                if self.cfg.script.power_strip(v, " ")
            )

        # sql parsing
        # -----------
        stripped_sql = self.cfg.script.power_strip(
            val_to_strip=sql,
            chars_to_strip="\n ",  # trailing lines and whitespace
        )
        self.first_line = self.cfg.script.power_strip(
            val_to_strip=stripped_sql.split('\n')[0].lower(),
            chars_to_strip='\n ',  # same for first line only
        )
        self.words_in_first_line = [
            self.cfg.script.arg_to_string(v)
            for v in self.first_line.split(' ')
            if self.cfg.script.arg_to_string(v)
        ]
        self.first_line_remainder = " ".join(
            self.words_in_first_line[1:]
            if len(self.words_in_first_line) >= 2 else str()
        )

        # set 'combined` attributes
        # -------------------------
        self.kw_ge = self.cfg.sql.kw_exceptions.get(
            self.words_in_first_line[0], self.words_in_first_line[0]
        )
        self.matched_terms = self.cfg.sql.objects_within(self.first_line)
        self.kw = self.kw_pr or self.kw_ge
        self.nm = self.nm_pr or self.nm_ge
        self.obj = self.obj_pr or self.obj_ge
        self.desc = self.desc_pr or self.desc_ge
        self.anchor = self.anchor_pr or self.anchor_ge

        # then create scope
        # -----------------
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

    @property
    def obj_ge(self):
        """Generated `object` for statement."""
        return (
            self.matched_terms[min(self.matched_terms)] if self.matched_terms
            else self.cfg.DEF_OBJ
        )

    @property
    def desc_ge(self):
        """Generated `description` for statement."""
        idx_str = f" #{self.index}" if self.incl_idx_in_desc else str()
        return f"{self.cfg.DEF_DESC}{idx_str}"

    @property
    def anchor_ge(self):
        """Generated `anchor` for statement."""
        generalized_anchor = self.cfg.sql.generic_anchors.get(self.kw_ge)
        if (
            generalized_anchor
            and self.obj_ge == self.cfg.DEF_OBJ
        ):
            return generalized_anchor
        s = ' ' if self.kw_ge and self.obj_ge else ''
        return f"{self.kw_ge}{s}{self.obj_ge}"

    @property
    def nm_ge(self):
        """Generated `name`; full statement tag for statement."""
        return f"{self.anchor_ge}{self.patt.core.sep_desc}{self.desc_ge}"

    def __bool__(self) -> bool:
        return self.is_included

    def __str__(self) -> str:
        return f"statement.Tag(nm='{self.nm}')"

    def __repr__(self) -> str:
        return f"statement.Tag(nm='{self.nm}')"
