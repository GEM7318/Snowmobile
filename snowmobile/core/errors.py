"""
Base Snowmobile exception class.
"""
from typing import Dict, Optional
import time


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
        prefix: str = None,
        sep: str = None,
        lines: int = None,
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
