"""
Base class for user-facing objects (i.e. classes that are **not** derived from
pydantic's BaseModel).
"""
from __future__ import annotations


class Snowmobile:
    """Generic dunder implementation for ``snowmobile`` objects.

    Base class for all ``snowmobile`` objects that do **not** inherit from
    pydantic's BaseModel or configuration class, :class:`Config`.

    """
    def __init__(self):
        pass

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __str__(self):
        return f"snowmobile.{type(self).__name__}()"

    def __repr__(self):
        return str(self)
