"""
snowmobile.Script exceptions.
"""
from typing import Optional, List

from snowmobile.core import errors


class StatementNotFoundError(errors.Error):
    """Exceptions due to an invalid statement name or index."""

    def __init__(
        self,
        nm: str,
        statements: List[str] = None,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)
        self.st = statements

    def __str__(self):
        """StatementNotFoundError message."""
        statements = ", ".join(f"'{s}'" for s in self.st) if self.st else ""
        str_args = self.format_error_args(
            _filter=True,
            **{
                "name-provided": f"'{self.nm}'",
                "msg": self.msg,
                "errno": self.errno,
                "names-found": statements,
            },
        ).strip("\n")
        return f"""
Statement name or index, `{self.nm}`, is not found in the script.
{str_args}
"""


class DuplicateTagError(errors.Error):
    """Exceptions due to a duplicate statement tag."""

    def __init__(
        self,
        nm: str,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """DuplicateTagError message."""
        str_args = self.format_error_args(
            _filter=True,
            **{"name": f"'{self.nm}'", "msg": self.msg, "errno": self.errno},
        ).strip("\n")
        return f"""
indistinct statement names found within {self.nm}; tag names must be unique if
running `script.contents(by_index=False)`.
see contents of `script.duplicates` for the exact tag names causing the issue.
"""