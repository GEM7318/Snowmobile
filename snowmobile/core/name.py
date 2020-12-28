"""
Represents a single attribute name.
"""
from __future__ import annotations

from typing import Optional

from . import Snowmobile, Configuration


# TESTS: Add tests for Name
class Name(Snowmobile):
    """Handles attribute-name parsing including identification of wildcards.

    """

    def __init__(
            self,
            nm: str,
            cfg: Configuration,
            is_title: Optional[bool] = None
    ):
        super().__init__()

        cfg_md = cfg.script.markdown
        cfg_script = cfg.script

        self.nm_raw = nm
        self.nm_stripped, self.flags = cfg.wildcards.partition_on_wc(attr_nm=nm)
        self.specified_position = cfg.attrs.get_position(attr=self.nm_stripped)

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
            self.nm_adj = (
                self.nm_stripped.title() if not is_title
                else self.nm_stripped
            )


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
        return f"Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"

    def __str__(self):
        return f"Name(nm='{self.nm_raw}', nm_adj='{self.nm_adj}')"
