"""
Base class for all :class:`Statement` objects.
"""
from __future__ import annotations

import re
from typing import Dict

from . import Generic


class Scope(Generic):
    """Handles the scope/context for :class:`Statement` objects and derived classes.

    Should never be interacted with from the user-facing API.

    Attributes:
        base (str):
            The left-most word within a statement tag. For **generic**
            statements this will be the `keyword` and for **QA** statements
            this will be the literal word ``qa``.
        component (str):
            The component within a given tag that is being evaluated; this will
            be exactly **one** of `kw`, `obj`, `anchor`, `desc`, or `nm`.
        incl_arg (str):
            The keyword argument that would be used to exclude a given
            component;
                *   e.g. if :attr:`component` is `kw`, :attr:`incl_arg` would
                    be ``incl_kw``.
        excl_arg (str):
            The keyword argument that would be used to exclude a given
            component; this would be the same as the above example except
            the value would be ``excl_kw`` as opposed to ``incl_kw``.
        fallback_to (dict):
            The default values to fall back to for :attr:`incl_arg` and
            :attr:`excl_arg` if they are not passed as a keyword argument
            by the user in :class:`Script`; defaults to including the
            :attr:`base` and excluding an empty list.
        provided_args (dict):
            The set of keyword arguments provided at the time of the last call
            to :meth:`eval()`.
        check_against_args (dict):
            The set of keyword arguments checked against at the time of the
            last call to :meth:`eval()`; will use provided arguments if they
            exist and the arguments from :attr:`fallback_to` otherwise.
        is_included (bool):
            Tag is included based on the results of the last call to
            :meth:`eval()`.
        is_excluded (bool):
            Tag is excluded based on the results of the last call to
            :meth:`eval()`.

    """

    def __init__(self, arg: str, base: str):
        """Instantiates a :class:`Scope` object."""
        super().__init__()
        self.component: str = arg  # 'kw'
        self.base = base.lower()  # 'qa'
        self.incl_arg = f"incl_{arg}"  # 'incl_kw'
        self.excl_arg = f"excl_{arg}"  # 'excl_kw'
        self.fallback_to: Dict = {self.incl_arg: [base], self.excl_arg: list()}
        self.provided_args: Dict = dict()
        self.check_against_args: Dict = dict()
        self.is_included: bool = bool()
        self.is_excluded: bool = bool()

    def parse_kwargs(self, **kwargs) -> None:
        """Parses all filter arguments looking for those that match its base.

        Looks for include/exclude arguments within kwargs, populating
        :attr:`provided_args` with those that were provided and populates
        :attr:`check_against_args` with the same values if they were provided
        and fills in defaults from :attr:`fallback_to` otherwise.

        Args:
            **kwargs:
                Keyword arguments passed to :class:`Script.filter()` (e.g.
                `incl_kw`, `excl_kw`, ..)
        """
        self.provided_args = {
            k: v for k, v in kwargs.items() if k in [self.incl_arg, self.excl_arg]
        }
        self.check_against_args = {
            k: (self.provided_args.get(k) or self.fallback_to[k])
            for k in [self.incl_arg, self.excl_arg]
        }

    def matches_patterns(self, arg: str) -> bool:
        """Returns indication of if :attr:`base` matches a given set of patterns.

        Args:
            arg (str):
                Will either be the value of :attr:`incl_arg` or
                :attr:`exclude_arg`.

        Returns (bool):
            Indication of whether any matches were found.

        """
        escaped = any(
            re.findall(pattern=re.escape(self.base), string=p)
            for p in self.check_against_args[arg]
        )
        unescaped = any(
            re.findall(string=self.base, pattern=p)
            for p in self.check_against_args[arg]
        )
        return any([escaped, unescaped])

    @property
    def included(self):
        """Tag is included based on results of last :meth:`eval()`."""
        return self.is_included and not self.is_excluded

    def eval(self, **kwargs) -> bool:
        """Evaluates filter arguments and updates context accordingly.

        Updates the values of :attr:`is_included`, :attr:`is_excluded`, and
        :attr:`included`.

        Args:
            **kwargs:
                Keyword arguments passed to :class:`Script.filter()` (e.g.
                `incl_kw`, `excl_kw`, ..)

        Returns (bool):
            Indicator of whether or not the statement should be
            included/excluded based on the context/keyword arguments provided.

        """
        self.parse_kwargs(**kwargs)
        self.is_included = self.matches_patterns(arg=self.incl_arg)
        self.is_excluded = self.matches_patterns(arg=self.excl_arg)
        return self.included

    def __str__(self) -> str:
        return (
            f"Scope(arg='{self.component}', base='{self.base}', "
            f"included={self.included})"
        )

    def __repr__(self) -> str:
        return f"Scope(arg='{self.component}', base='{self.base}')"

    def __bool__(self) -> bool:
        """Mirrors the state of :attr:`included`."""
        return self.included
