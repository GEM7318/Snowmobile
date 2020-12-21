"""
:class:`Column` object. Purpose is..
"""
from __future__ import annotations

import itertools
import re
import string
from contextlib import contextmanager


# DOCSTRING
class Column:
    """Handles the transformation of a single column within a DataFrame."""

    _EXCLUDE_CHARS = list(
        itertools.chain.from_iterable(
            (
                [c for c in string.punctuation if c != "_"],
                [w for w in string.whitespace],
            )
        )
    )

    def __init__(
        self, original: str, current: str = None, prior: str = None, src: str = None,
    ):
        self.original = original
        self.src = src or "original"
        self.current = current or self.original
        self.prior = prior or self.current

    @contextmanager
    def update(self):
        try:
            self.prior = self.current
            yield self
        finally:
            return self.current

    def lower(self) -> str:
        with self.update() as s:
            s.current = s.current.lower()
        return self.current

    def upper(self) -> str:
        with self.update() as s:
            s.current = s.current.upper()
        return self.current

    def reformat(self, fill_char: str = None, dedupe_special: bool = True) -> str:
        with self.update() as s:
            fill_char = fill_char or "_"
            to_swap = {k: fill_char for k in self._EXCLUDE_CHARS}
            for char, swap_char in to_swap.items():
                s.current = s.current.replace(char, swap_char)
            if dedupe_special:
                s.current = s.dedupe(fill_char, s.current)
        return self.current

    @staticmethod
    def dedupe(char: str, to_dedupe: str) -> str:
        matches = re.findall(f"{char}+", to_dedupe)
        for match in reversed(matches):
            to_dedupe = to_dedupe.replace(match, char)
        return to_dedupe

    def __setattr__(self, key, value):
        vars(self)[key] = value

    def __setitem__(self, key, value):
        vars(self)[key] = value

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
