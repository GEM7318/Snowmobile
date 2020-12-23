"""
snowmobile Exception classes.
"""
from typing import Optional

from snowmobile.core import errors


class StatementInternalError(errors.InternalError):
    """Internal error class for Statement and derived classes."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)


class StatementPostProcessingError(errors.Error):
    """Exceptions that occur in the post-processing invoked by `s.process()`.

	Indicates a non-database error occurred in the over-ride :meth:`process()`
	method from a derived class of :class:`Statement`.

	"""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """StatementPostProcessingError message."""
        return (
            f"An error was encountered during post-processing '{self.msg}'"
            if self.msg
            else f"Post-processing error encountered"
        )


class QAFailure(errors.Error):
    """Exceptions that occur in post-processing invoked by `s.process()`.

	Indicates a non-database error occurred in the :meth:`process()` over-ride
	method of :class:`Statement`'s derived classes.

	Args:
		nm (str):
			Tag name of QA statement.
		desc (str):
			Object-specific exception message to display.
		idx (int):
			Index of the statement that failed its QA check.

	"""

    def __init__(
        self,
        nm: str,
        msg: str,
        idx: int,
        desc: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(msg=msg, errno=errno, nm=nm, to_raise=to_raise)
        self.desc = desc
        self.idx = idx

    def __str__(self):
        """QAFailure message."""
        str_args = self.format_error_args(
            _filter=True,
            **{
                "name": f"'{self.nm}' (statement #{self.idx})",
                "msg": self.msg,
                "user-description": self.desc,
            },
        ).strip("\n")
        return f"""
A configured QA check did not pass its validation:
{str_args}
"""


class QAEmptyFailure(QAFailure):
    """Exception class for `qa.Empty` statements."""

    def __init__(
        self,
        nm: str,
        msg: str,
        idx: int,
        desc: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(
            nm=nm, msg=msg, idx=idx, desc=desc, errno=errno, to_raise=to_raise
        )


class QADiffFailure(QAFailure):
    """Exception class for `qa.Empty` statements."""

    def __init__(
        self,
        nm: str,
        msg: str,
        idx: int,
        desc: Optional[str] = None,
        errno: Optional[int] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(
            nm=nm, msg=msg, idx=idx, desc=desc, errno=errno, to_raise=to_raise
        )
