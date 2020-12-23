"""
Statement and embedded objects.
"""
__all__ = [
    "Empty",
    "Diff",
    "Statement",
    "Scope",
    "Tag",
    "QADiffFailure", "QAEmptyFailure", "QAFailure",
    "StatementPostProcessingError", "StatementInternalError",
]
from .qa import Diff, Empty, QADiffFailure, QAEmptyFailure
from .errors import (
    QAFailure,
    StatementPostProcessingError,
    StatementInternalError,
)
from .statement import Statement
from .scope import Scope
from .tag import Tag
