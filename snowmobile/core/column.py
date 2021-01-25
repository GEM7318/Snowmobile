"""
Represents a single ``Column`` of a {class}`SnowFrame`}.
"""
from __future__ import annotations

import itertools
import re
import string
from contextlib import contextmanager
from typing import Optional

from . import Generic


class Column(Generic):
    """Handles transformation operations of a single column within a DataFrame."""

    _EXCLUDE_CHARS = list(
        itertools.chain.from_iterable(
            (
                [c for c in string.punctuation if c != "_"],
                [w for w in string.whitespace],
            )
        )
    )

    def __init__(
        self,
        original: str,
        current: Optional[str] = None,
        prior: Optional[str] = None,
        src: Optional[str] = None,
    ):
        super().__init__()
        self.original = original
        self.src = src or "original"
        self.current = current or self.original
        self.prior = prior or self.current

    @contextmanager
    def update(self):
        """Simple context manager for dealing with current/prior migration."""
        try:
            self.prior = self.current
            yield self
        finally:
            return self.current

    def lower(self) -> str:
        """Lower case column."""
        with self.update() as s:
            s.current = s.current.lower()
        return self.current

    def upper(self) -> str:
        """Upper case column."""
        with self.update() as s:
            s.current = s.current.upper()
        return self.current

    @staticmethod
    def dedupe(current: str, char: Optional[str] = None) -> str:
        """Dedupes consecutive characters within a string.

        Note:
            *   Must iterate through matches and perform replacements in the
                order of the **largest to the smallest by number of characters**;
                this is to avoid altering the matches found before replacing them.

        Args:
            current (str):
                String containing characters to dedupe.
            char (str):
                Character to dedupe.

        """
        matches = re.findall(f"{char}+", current)

        for match in reversed(matches):
            current = current.replace(match, char)
        return current

    def reformat(
        self, fill_char: Optional[str] = None, dedupe_special: bool = True
    ) -> str:
        """Reformat column for a load to the database.

        Args:
            fill_char (str):
                Character to replace special characters and whitespace with;
                defaults to `_`.
            dedupe_special (bool):
                Dedupe consecutive special characters; defaults to `True`.

        """
        with self.update() as s:
            fill_char = fill_char or "_"
            to_swap = {k: fill_char for k in self._EXCLUDE_CHARS}
            to_swap['_'] = '_'
            for char, swap_char in to_swap.items():
                s.current = s.current.replace(char, swap_char)
            if dedupe_special:
                s.current = s.dedupe(current=s.current, char=fill_char)
        return self.current

    def __eq__(self, other: Column) -> bool:
        return all(
            (
                self.original == other.original,
                self.src == other.src,
                self.current == other.current,
                self.prior == other.prior,
            )
        )

    def __str__(self) -> str:
        return f"Column(current='{self.current}')"

    def __repr__(self) -> str:
        return f"Column(original='{self.original}', current='{self.current}')"
