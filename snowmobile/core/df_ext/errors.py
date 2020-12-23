"""
:class:`SnowFrame` exception class.
"""
from typing import Optional

from snowmobile.core import errors


class SnowFrameInternalError(errors.InternalError):
    """Internal error class for 'class:`SnowFrame`."""

    def __init__(
        self,
        msg: Optional[str] = None,
        errno: Optional[int] = None,
        nm: Optional[str] = None,
        to_raise: Optional[bool] = False,
    ):
        super().__init__(nm=nm, msg=msg, errno=errno, to_raise=to_raise)
