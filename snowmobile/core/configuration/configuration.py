"""
Module handles:
    * Exporting an initial configuration file
    * Locating a populated configuration file
    * Caching of this location
    * Parsing/instantiating the full configuration object
"""
from __future__ import annotations

import shutil
import json
from pathlib import Path
from typing import Dict, Union, Any, Callable
from types import MethodType

import toml
from fcache.cache import FileCache
from pydantic.json import pydantic_encoder

from ._stdout import Configuration as Stdout
from .schema import Snowmobile, Base

# ====================================
# Mapping to package data directory
HERE = Path(__file__).absolute()
MODULE_DIR = HERE.parent.parent
PACKAGE_DATA = MODULE_DIR / "pkg_data"

# Defaults paths for DDL and backend extension
SPEC_BACKEND = PACKAGE_DATA / "snowmobile_backend.toml"
DDL = PACKAGE_DATA / "DDL.sql"
# ====================================


class Cache(FileCache):
    """Handles caching of paths to configuration files."""

    def __init__(self, application: str = "snowmobile"):

        application: str = application
        flag: str = "cs"
        super().__init__(appname=application, flag=flag)

    def save(self, item_name: str, item_value):
        """Caches `item_value` to be retrieved by `item_name`."""
        self[item_name] = str(item_value)
        return self

    # noinspection PyMethodOverriding
    def delete(self, item_name: str) -> Cache:
        """Deletes `item_name` from cache."""
        if self.get(item_name):
            self.pop(item_name)
        return self

    def as_path(self, item_name: str):
        """Utility to return `item_name` as a :class:`Path` object."""
        return Path(self.get(item_name)) if self.get(item_name) else None


class Configuration(Snowmobile):

    _stdout = Stdout()

    # -- Statement components to be considered for scope.
    SCOPE_ATTRIBUTES = [
        "kw",
        "obj",
        "desc",
        "anchor",
        "nm",
    ]
    SCOPE_TYPES = [
        "incl",
        "excl",
    ]

    # -- e.g. populates associated parts of 'insert into-unknown~statement #2'
    DEF_OBJ = "unknown"
    DEF_DESC = "statement"

    # -- Anchors to associate with QA statements.
    QA_ANCHORS = {
        "qa-diff",
        "qa-empty",
    }

    # -- Package data directory
    PKG_DATA = MODULE_DIR / "pkg_data"

    def __init__(
        self,
        config_file_nm: str = None,
        creds: str = None,
        from_config: Path = None,
        export_dir: Path = None,
    ):
        """Instantiates instances of the needed params to locate creds file.

        Args:
            config_file_nm (str):
                Name of .toml configuration file following the format of
                ``snowmobile_SAMPLE.toml`` (defaults to `snowmobile.toml`).
            creds (str):
                Name of connection within [credentials] section of .toml file
                to use, defaults to the first set of credentials if creds
                isn't explicitly passed.
            from_config (Union[str, Path]):
                Optionally pass in a full pathlib.Path object to a specific
                `.toml` configuration file matching the format of
                `snowmobile_SAMPLE.toml`.

        """
        self.file_nm = config_file_nm or "snowmobile.toml"
        self.cache = Cache()

        if export_dir:
            self._stdout.exporting(file_name=self.file_nm)
            export_dir = export_dir or Path.cwd()
            export_path = export_dir / self.file_nm
            template_path = PACKAGE_DATA / "snowmobile_TEMPLATE.toml"
            shutil.copy(template_path, export_path)
            self._stdout.exported(file_path=export_path)

        else:
            self.location: Path = (
                Path(str(from_config))
                if from_config
                else Path(str(self.cache.get(self.file_nm)))
            )

            self.creds = creds.lower() if creds else ""

            try:
                path_to_config = self._get_path(is_provided=bool(from_config))
                with open(path_to_config, "r") as r:
                    cfg = toml.load(r)

                if self.creds:
                    cfg["connection"]["default-creds"] = self.creds

                # TODO: Add sql export disclaimer to this as well
                if not cfg["external-file-locations"].get("ddl"):
                    cfg["external-file-locations"]["ddl"] = DDL
                if not cfg["external-file-locations"].get("backend-ext"):
                    cfg["external-file-locations"]["backend-ext"] = SPEC_BACKEND

                super().__init__(**cfg)

            except IOError as e:
                raise IOError(e)

    def _get_path(self, is_provided: bool = False):
        """Checks for cache existence and validates - traverses OS if not.

        Args:
            is_provided (bool):
                Indicates whether or not ``from_config`` is populated or if
                configuration file is intended to come from cache or from
                a bottom-up traversal of the file system if not yet cached.
        """
        self._stdout.locating(is_provided)
        if self.location.is_file():
            self._stdout.found(file_path=self.location, is_provided=is_provided)
            return self.location
        else:
            self._stdout.not_found(creds_file_nm=self.file_nm)
            return self._find_creds()

    def _find_creds(self) -> Path:
        """Traverses file system from ground up looking for creds file."""

        found = None
        try:
            rents = [p for p in Path.cwd().parents]
            rents.insert(0, Path.cwd())
            for rent in rents:
                if list(rent.rglob(self.file_nm)):
                    found = list(rent.rglob(self.file_nm))[0]
                    break
            if found.is_file():
                self.location = found
                self.cache.save(item_name=self.file_nm, item_value=self.location)
                self._stdout.file_located(file_path=self.location)
                return self.location

        except IOError as e:
            self._stdout.cannot_find(self.file_nm)
            raise IOError(e)

    @staticmethod
    def batch_set_attrs(obj: Any, attrs: dict, to_none: bool = False):
        """Batch sets attributes on an object from a dictionary.

        Args:
            obj (Any):
                Object to set attributes on.
            attrs (dict):
                Dictionary containing attributes.
            to_none (bool):
                Set all of the object's attributes batching a key in ``attrs``
                to `None`; defaults ot `False`.

        Returns (Any):
            Object post-setting attributes.

        """
        for k in set(vars(obj)).intersection(attrs):
            setattr(obj, k, None if to_none else attrs[k])
        return obj

    @staticmethod
    def methods_from_obj(obj: Any) -> Dict[str, MethodType]:
        """Utility to return methods from an object as a dictionary."""
        return {
            str(m): getattr(obj, m)
            for m in dir(obj)
            if isinstance(getattr(obj, m), MethodType)
        }

    @staticmethod
    def attrs_from_obj(obj: Any) -> Dict[str, MethodType]:
        """Utility to return attributes/properties from an object as a dictionary."""
        return {
            str(m): getattr(obj, m)
            for m in dir(obj)
            if not isinstance(getattr(obj, m), Callable)
        }

    # TODO: Stick somewhere that makes sense
    @property
    def scopes(self):
        """All combinations of scope type and scope attribute."""
        return {
            f"{typ}_{attr}": set()
            for typ in self.SCOPE_TYPES
            for attr in self.SCOPE_ATTRIBUTES
        }

    def scopes_from_kwargs(self, **kwargs) -> Dict:
        """Accepts a dict of keyword arguments and returns a full dictionary of
        scopes, including empty sets for those not included in kwargs."""
        scopes = {}
        for attr in self.scopes:
            attr_value = kwargs.get(attr) or set()
            scopes[attr] = attr_value
        return scopes

    def __str__(self):
        return f"snowmobile.Configuration('{self.file_nm}')"

    def __repr__(self):
        return f"snowmobile.Configuration(config_file_nm='{self.file_nm}')"

    def __json__(self, by_alias: bool = False, **kwargs):
        return self.json(by_alias=by_alias, **kwargs)

    def json(self, by_alias: bool = False, **kwargs):
        """Combined serialization method for pydantic attributes."""
        total = {}
        for k, v in vars(self).items():
            if issubclass(type(v), Base):
                total = {**total, **v.as_serializable(by_alias=by_alias)}
        return json.dumps(obj=total, default=pydantic_encoder, **kwargs)
