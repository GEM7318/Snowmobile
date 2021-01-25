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

        ## (1) create-table~dummy_name *[contents get 'h2' level headers]
        ----

        - **Tag1**: Value1       *[tags can also be validations arguments..
        - **Arg1**: Val2          [that snowmobile will run on the sql results]

        **Description**          *[contents get one of these too]

        **SQL**                  *[their rendered sql does as well]
            ...sql
                ...
                ...
            ...


        ## (2) update-table~dummy_name2
        ----
        [structure repeats for all contents in the script]

        ```

"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from . import Generic, Configuration, Snowmobile, Diff, Empty, Section, Statement
from .paths import DIR_PKG_DATA
from .cfg import Marker
from .utils import Console


class Markup(Generic):
    """Markup document from SQL script.
    """

    def __init__(
        self,
        sn: Snowmobile,
        path: Path,
        contents: Dict[int, Union[Statement, Marker]],
        alt_file_nm: Optional[str] = None,
        alt_file_prefix: Optional[str] = None,
        alt_file_suffix: Optional[str] = None,
        incl_sql: bool = True,
        incl_markers: bool = True,
        incl_raw: bool = False,
        sql_incl_export_disclaimer: bool = True,
    ):
        super().__init__()
        self._stdout = Console()
        self.pkg_data_dir = DIR_PKG_DATA
        self.contents = contents
        self.cfg: Configuration = sn.cfg
        self.alt_file_nm: str = alt_file_nm or str()
        self.alt_file_prefix: str = alt_file_prefix or str()
        self.alt_file_suffix: str = alt_file_suffix or str()
        self.sql_incl_export_disclaimer: bool = sql_incl_export_disclaimer
        self.incl_markers: bool = incl_markers
        self.incl_sql = incl_sql
        self.incl_raw = incl_raw
        self.exported: List[Path] = list()
        self.created: List[Path] = list()
        self.path = Path(str(path)) if path else Path()

    @property
    def doc_root(self) -> Path:
        """Documentation sub-directory; `.snowmobile` by default."""
        return (
            # Path()
            # if not self.path.anchor
            # else
            self.path.parent
            / self.cfg.script.export_dir_nm
        )

    @property
    def _file_nm(self) -> str:
        """Generic file name of script."""
        return self.alt_file_nm or self.path.name

    @property
    def _file_nm_components(self) -> Tuple[str, str]:
        """Utility for easy access to the stem and the extension of file name."""
        stem, _, ext = self._file_nm.rpartition(".")
        return stem, ext

    @property
    def file_nm_sql(self) -> str:
        """Adjusted file name of the exported sql script."""
        stem, ext = self._file_nm_components
        return f"{self.alt_file_prefix}{stem}{self.alt_file_suffix}.{ext}"

    @property
    def file_nm_md(self) -> str:
        """Adjusted file name of the exported markdown."""
        stem, ext = self._file_nm_components
        return f"{self.alt_file_prefix}{stem}{self.alt_file_suffix}.md"

    @property
    def script_dir(self) -> Path:
        """Directory for all exports from specific _file_nm.."""
        stem, _, ext = self._file_nm.rpartition(".")
        return self.doc_root / stem

    @property
    def path_md(self) -> Path:
        """Full path to write markdown to."""
        return self.script_dir / self.file_nm_md

    @property
    def path_sql(self) -> Path:
        """Full path to write sql """
        return self.script_dir / self.file_nm_sql

    @property
    def sections(self) -> Dict[int, Section]:
        """All header sections of markdown file as a dictionary."""
        sections = {}
        for i, s in self.contents.items():
            if self._is_statement(s=s):  # create section from statement.section()
                sections[i] = s.as_section(self.incl_raw)
            else:
                sections[i] = Section(  # create section from marker metadata
                    incl_raw=self.incl_raw,
                    is_multiline=True,
                    cfg=self.cfg,
                    raw=s.raw,
                    **s.as_args(),
                )

        return {i: sections[i] for i in sorted(sections)}

    @property
    def markdown(self) -> str:
        """Full markdown file as a string."""
        included = self.included
        return "\n\n".join(s.md for i, s in self.sections.items() if i in included)

    @property
    def _export_disclaimer(self) -> str:
        """Block comment disclaimer of export at top of exported sql file."""
        path_to_sql_txt = self.pkg_data_dir / "sql_export_heading.txt"
        with open(path_to_sql_txt, "r") as r:
            header = r.read()
        return f"{header}" if self.sql_incl_export_disclaimer else str()

    @property
    def included(self):
        """All included indices based on incl_ attributes."""
        return {
            i
            for i, s in self.contents.items()
            if (
                (self.incl_sql and self._is_statement(s=s))
                or (self.incl_markers and not self._is_statement(s=s))
            )
        }

    @property
    def sql(self):
        """SQL for export."""
        to_export = [
            s.trim()
            if self._is_statement(s)
            else self.cfg.script.as_parsable(raw=s.raw, is_marker=True)
            for i, s in self.contents.items()
            if i in self.included
        ]
        if self.sql_incl_export_disclaimer:
            to_export.insert(0, self._export_disclaimer)
        return "\n".join(to_export)

    @staticmethod
    def _is_statement(s: Union[Statement, Diff, Empty, Marker]) -> bool:
        """Utility to check if a given instance of contents is a statement."""
        return isinstance(s, (Statement, Diff, Empty))

    def _scaffolding(self) -> None:
        """Ensures directory scaffolding exists before attempting export."""
        if not self.script_dir.exists():
            self.script_dir.mkdir(parents=True)
            self.created.append(self.script_dir)

    def _export(self, path: Path, val: str):
        """Ensure directory scaffolding exists and writes a string to a path (.sql or .md)."""
        self._scaffolding()
        with open(path, "w") as f:
            f.write(val)
            self.exported.append(path)
            self._stdout.offset_path(
                file_path=path, root_dir_nm=path.parent.name, indent="\t", output=True
            )

    def export(self, md_only: bool = False, sql_only: bool = False) -> None:
        """Export files.

        Args:
            md_only (bool): Export markdown file only.
            sql_only (bool): Export sql file only.

        """

        def _md():
            self._export(path=self.path_md, val=self.markdown)

        def _sql():
            self._export(path=self.path_sql, val=self.sql)

        if md_only:
            _md()
        elif sql_only:
            _sql()
        else:
            _md()
            _sql()

    def __call__(self, **kwargs):
        """Batch setattr function for all keywords matching Markup's attributes."""
        return self.cfg.batch_set_attrs(obj=self, attrs=kwargs)

    def __str__(self) -> str:
        return f"script.Markup('{self.file_nm_sql}')"

    def __repr__(self) -> str:
        return f"script.Markup('{self.file_nm_sql}')"
