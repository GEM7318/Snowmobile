"""
Statement and embedded objects.
"""
__all__ = [
	"Empty",
	"Diff",
	"Statement",
	"Scope",
	"Tag",
]
from .diff import Diff
from .empty import Empty
from .statement import Statement
from .scope import Scope
from .tag import Tag
