"""
Exceptions for :class:`Loader`..
"""
from typing import Optional

from snowmobile.core import errors


class LoadingValidationError(errors.Error):
    """Exception class for errors that occur while validating a table load."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)

    def __str__(self):
        """LoadingValidationError message."""
        str_args = self.format_error_args(
            _filter=True, **{"name": self.nm, "msg": self.msg,},
        ).strip("\n")
        return f"""
An error has occurred during validation of the data load.
{str_args}
"""


class LoadingInternalError(errors.InternalError):
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
