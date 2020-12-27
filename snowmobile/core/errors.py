"""
Snowmobile exceptions.
"""
import time
from typing import Dict, Optional, List


class Error(Exception):
    """Base Snowmobile exception class.

    Args:
        msg (Optional[str]):
            Error message.
        msg (Optional[int]):
            Error number.
        nm (Optional[str]):
            Globally unique name for an exception being raised; used for
            InternalExceptions and statement names when QA failures occur.
        to_raise (Optional[bool]):
            Indicates that the exception should be raised before exiting the
            current context.

    Attributes:
        tmstmp (int):
            Unix instantiation timestamp of the exception (in seconds).
        raised (bool):
            Indicator of whether or not the instance has already been raised;
            used for exception chaining from Statement -> Script.

    """

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        self.tmstmp: int = int(time.time())
        self.msg = msg
        self.errno = errno
        self.nm = nm
        self.to_raise: bool = to_raise
        self.raised: bool = False

    def __str__(self):
        """Default error message."""
        return f"{self.msg}" if self.msg else f"Exception encountered"

    def escalate(self):
        """Raises error."""
        self.raised = True
        raise self

    @staticmethod
    def format_error_args(
        prefix: Optional[str] = None,
        sep: Optional[str] = None,
        lines: Optional[int] = None,
        _filter: bool = True,
        **kwargs: Dict[str, str],
    ) -> str:
        """Formats a dictionary of arguments into an aligned/indented error msg.

        Placed below primary msg such that a primary msg of 'This is a __ error.'
        combined with the returned value from this method provided with
        kwargs={'argument-description1': 'argument-value', 'arg2-desc': 'arg2-value'}
        would produce the following error message:
            ```
            This is a __ error.
                argument-description: argument-value
                           arg2-desc: arg2-value
            ```

        Args:
            prefix (str):
                Character to prefix bullets with; defaults to '\t'.
            sep (str):
                Character to separate arguments/values with; defaults to ':'.
            lines (int):
                Number of lines to include between arguments; defaults to 1.
            _filter (bool):
                Indicator of whether to filter out key/value pairs that contain
                empty values; defaults to `True`.
            **kwargs:
                Argument keys and values to be converted into a list.

        Returns (str):
            Formatted arguments as a string.

        """
        prefix = prefix or "\t"
        line_sep = "\n" * (lines or 1)
        sep = sep or ": "

        if _filter:
            kwargs = {k: v for k, v in kwargs.items() if v}

        longest = max(len(k) for k in kwargs)
        args = [
            f"{prefix}{k.rjust(len(k) + (longest-len(k)))}{sep}{v}"
            for k, v in kwargs.items()
        ]

        return line_sep.join(args)


class InternalError(Error):
    """Internal error class for detection/testing of edge-case exceptions.

    """

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """InternalError message."""
        str_args = self.format_error_args(
            _filter=True,
            **{"name": f"'{self.nm}'", "msg": self.msg, "errno": self.errno,},
        ).strip("\n")
        return f"""
An internal exception was raised.
{str_args}
"""


class StatementInternalError(InternalError):
    """Internal error class for Statement and derived classes."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)


class StatementPostProcessingError(Error):
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


class QAFailure(Error):
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


class SnowFrameInternalError(InternalError):
    """Internal error class for 'class:`SnowFrame`."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """SnowFrameInternalError message."""
        str_args = self.format_error_args(
            _filter=True, **{"name": self.nm, "msg": self.msg,},
        ).strip("\n")
        return f"""
{str_args}
"""


class StatementNotFoundError(Error):
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


class DuplicateTagError(Error):
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


class LoadingInternalError(InternalError):
    """Exception class for errors boundary exception detection while loading."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """LoadingInternalError message."""
        str_args = self.format_error_args(
            _filter=True, **{"name": self.nm, "msg": self.msg,},
        ).strip("\n")
        return f"""
An internal exception was encountered in `snowmobile.Table`.
{str_args}
"""


class ExistingTableError(Error):
    """Table exists and `if_exists=Fail`"""

    pass


class ColumnMismatchError(Error):
    """Columns do not match and `if_exists!='replace'`"""

    pass


class FileFormatNameError(StatementNotFoundError):
    """The name of the provided file format is invalid."""

    pass
