"""
Statement and embedded objects.
"""
__all__ = [
    "Empty",
    "Diff",
    "Statement",
    "Scope",
    "Tag",
    "QADiffFailure",
    "QAEmptyFailure",
    "QAFailure",
    "StatementPostProcessingError",
    "StatementInternalError",
]
from .errors import QAFailure, StatementInternalError, StatementPostProcessingError
from .qa import Diff, Empty, QADiffFailure, QAEmptyFailure
from .scope import Scope
from .statement import Statement
from .tag import Tag
