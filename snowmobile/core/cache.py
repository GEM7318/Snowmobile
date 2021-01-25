"""
Handles caching of the location of ``snowmobile.toml``.
"""
from __future__ import annotations

import json

from pathlib import Path
from typing import Dict, List, Union, ContextManager, Any
from contextlib import contextmanager

from appdirs import AppDirs

from . import Generic
from snowmobile import (
    __version__ as version,
    __author__ as author,
    __application__ as application,
)


class Cache(Generic):
    """Bare bones caching implementation for configuration file locations."""

    def __init__(self):
        super().__init__()
        app_dirs = AppDirs(appname=application, appauthor=author, version=version)
        self.file_nm = f"{application}_cache.json"
        self.cache_dir = Path(app_dirs.user_cache_dir)
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(mode=0o777, parents=True, exist_ok=False)
        self.location = self.cache_dir / self.file_nm
        self.contents: Dict = dict()
        if self.location.exists():
            with open(self.location, "r") as r:
                self.contents = json.load(r)

    @contextmanager
    def save(self) -> ContextManager[Cache]:
        """Writes changes to disk when exiting context of other methods."""
        try:
            yield self
        except Exception as e:
            raise e
        finally:
            with open(self.location, "w") as f:
                f.write(json.dumps(self.contents, indent=2))

    def save_item(self, item_name: str, item_value):
        """Caches `item_value` to be retrieved by `item_name`."""

        def to_str(item: Any):
            """Returns a pathlib.Path object as a serializable string."""
            return item.as_posix() if isinstance(item, Path) else item

        with self.save() as s:
            s.contents[to_str(item_name)] = to_str(item_value)
        return self

    def save_all(self, items: Dict):
        """Caches a dictionary of items"""
        with self.save() as s:
            for k, v in items.items():
                s.save_item(k, v)
        return self

    def as_path(self, item_name: str) -> Path:
        """Utility to return `item_name` as a :class:`Path` object."""
        return Path(self.get(item_name)) if self.get(item_name) else None

    def clear(self, item: [List, str]):
        """Clears an item or a list of items from the cache by name."""
        with self.save() as s:
            if isinstance(item, str):
                item = [item]
            to_clear = list(s) if not item else set(s.contents).intersection(set(item))
            for k in to_clear:
                s.contents.pop(k)
        return self

    def contains(self, item: Union[List, str]) -> bool:
        """Checks if an item or list of items exist in the cache."""
        if isinstance(item, str):
            return bool(self.get(item))
        return all(i in self.contents for i in item)

    def get(self, item: str):
        """Fetch an item from contents."""
        return self.contents.get(item)

    def __str__(self) -> str:
        return f"Cache(application='{application}', items={len(self.contents)})"
