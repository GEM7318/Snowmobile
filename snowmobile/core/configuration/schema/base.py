"""
Configuration and Base classes from which all objects in snowmobile's
configuration model are derived (i.e. ``snowmobile.toml`` and
``snowmobile_backend.toml``.)
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path, WindowsPath
from typing import Any, Callable, Dict, Set

from pydantic import BaseModel, Extra
from pydantic.json import pydantic_encoder


class Config:
    """Configuration class for object model."""

    extra = Extra.allow
    allow_population_by_field_name = True
    allow_population_by_alias = True
    arbitrary_types_allowed = True
    json_encoders = {
        Path: lambda v: str(v.as_posix()),
        WindowsPath: lambda v: str(v.as_posix()),
        type: lambda v: str(v),
        Set: lambda v: list(v),
    }

    def apply_map_by_type(self, attrs: Dict, typ: Any, func: Callable):
        """Recursively apply function to all items of a dictionary of type 'typ'.

        Args:
            attrs (dict):
                Dictionary to traverse.
            typ (Type):
                Type of object to apply function to.
            func (Callable):
                Function to apply to values of type `typ`.

        Returns:
            Altered dictionary with function applied to all keys and values
            matching `typ`.

        """
        if isinstance(attrs, Mapping):
            return {
                self.apply_map_by_type(k, typ, func): self.apply_map_by_type(
                    v, typ, func
                )
                for k, v in attrs.items()
            }
        elif isinstance(attrs, typ):
            return func(attrs)
        else:
            return attrs

    def serialize(self, as_dict: Dict) -> Dict:
        """Recursively applies `json_encoder` functions to all items of a dictionary."""
        serializable = as_dict
        for typ, serialize_func in self.json_encoders.items():
            serializable = self.apply_map_by_type(
                attrs=serializable, typ=typ, func=serialize_func
            )
        return as_dict


class Base(BaseModel, Config):
    """Extension to pydantic's BaseModel, used a Base class for entire object model."""

    def from_relative(self, obj: Any):
        """Updates current object's attributes with those from a different
        instance of the same class."""
        for k in set(vars(obj)).intersection(set(vars(self))):
            vars(self)[k] = vars(obj)[k]
        return self

    def from_dict(self, args: Dict):
        """Accept a dictionary of arguments and updates the current object as if
        it were instantiated with those arguments."""
        return self.from_relative(obj=type(self)(**args))

    def as_serializable(self, by_alias: bool = False):
        """Returns a dictionary in serializable form."""
        return self.serialize(as_dict=self.dict(by_alias=by_alias))

    def json(self, by_alias: bool = False, **kwargs) -> str:
        """API-facing json serialization method."""
        return self.__json__(by_alias=by_alias, **kwargs)

    def __json__(self, by_alias: bool = False, **kwargs) -> str:
        """Custom serialization to handle sets and pathlib objects."""
        return json.dumps(
            obj=self.as_serializable(by_alias=by_alias),
            default=pydantic_encoder,
            **kwargs,
        )

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __setitem__(self, key, value):
        vars(self)[key] = value
