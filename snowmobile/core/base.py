"""
Base class for non-configuration objects (i.e. for all classes that are **not**
derived from pydantic's BaseModel).
"""
from __future__ import annotations


class Snowmobile(object):
    """Generic dunder implementation for ``snowmobile`` objects.

    Base class for all ``snowmobile`` objects that do **not** inherit from
    pydantic's BaseModel or configuration class, :class:`Config`.

    """

    def __init__(self):
        pass

    def __getattr__(self, item):
        return getattr(self, item)

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
