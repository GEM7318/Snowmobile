"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

from typing import Any, Iterable, Set, Type

from .errors import *
from . import Generic


class ExceptionHandler(Generic):
    """Context management for snowmobile objects."""

    def __init__(
        self,
        within: Optional[Any] = None,
        ctx_id: Optional[int] = None,
        in_context: bool = False,
        children: Dict[int, Any] = None,
        is_active_parent: bool = False,
        to_mirror: Optional[List[Any]] = None,
    ):
        super().__init__()
        self._ctx_id: Optional[int] = ctx_id

        self.within: Type = type(within) if within else None
        self.by_ctx: Dict[int, Dict[int, snowmobile_errors]] = dict()
        self.in_context: bool = in_context
        self.outcome: Optional[int] = None
        self.children = children
        self.is_active_parent: bool = is_active_parent
        self.to_mirror: Optional[List[Any]] = to_mirror

    @property
    def ctx_id(self):
        """Current context id."""
        if not self._ctx_id:
            self.set(ctx_id=time.time_ns())
        return self._ctx_id

    def set(
        self,
        ctx_id: Optional[int] = None,
        in_context: bool = False,
        outcome: Optional[int] = None,
    ):
        """**Set** attributes on self."""
        if ctx_id:
            if ctx_id in self.by_ctx and self:
                nm = self.within.__name__
                raise InternalError(
                    nm=f"ExceptionHandler.set() from within {nm}",
                    msg=f"an existing `_ctx_id`, {ctx_id}, was provided to `set(_ctx_id)`",
                )
            self._ctx_id = ctx_id if ctx_id != -1 else time.time_ns()
            self.by_ctx[self._ctx_id] = {}
        if in_context:
            self.in_context = in_context
        if outcome:
            self.outcome = outcome

        if self.is_active_parent and "set" in self.to_mirror:
            for child in self.children.values():
                child.e.set(ctx_id=ctx_id, in_context=in_context, outcome=outcome)

        return self

    def set_from(self, other: ExceptionHandler) -> ExceptionHandler:
        """Updates attributes from another ExceptionHandler object."""
        for k in ["_ctx_id", "in_context", "outcome"]:
            vars(self)[k] = vars(other)[k]
        return self

    def reset(
        self, ctx_id: bool = False, in_context: bool = False, outcome: bool = False
    ):
        """**Reset** attributes on self."""
        if ctx_id:
            self._ctx_id = None
        if in_context:
            self.in_context = False
        if outcome:
            self.outcome = None

        if self.is_active_parent and "reset" in self.to_mirror:
            for child in self.children.values():
                child.e.reset(ctx_id=ctx_id, in_context=in_context, outcome=outcome)

        return self

    @property
    def current(self):
        """All exceptions in the current context."""
        if not self._ctx_id:
            raise InternalError(
                nm="ExceptionalHandler.current",
                msg=f"""
A call was made to `.current` while the current value of '_ctx_id` is None.
""".strip(
                    "\n"
                ),
            )
        return self.by_ctx[self.ctx_id] if self.ctx_id in self.by_ctx else {}

    def collect(self, e: Any[snowmobile_errors]):
        """Stores an exception."""
        current = self.current
        current[int(time.time_ns())] = e
        self.by_ctx[self.ctx_id] = current
        return self

    def _first_last(self, idx: int):
        """Last exception encountered."""
        by_tmstmp = self.by_tmstmp
        return by_tmstmp[list(by_tmstmp)[idx]] if by_tmstmp else {}

    @property
    def first(self) -> Error:
        """First exception encountered."""
        return self._first_last(-1)

    @property
    def last(self) -> Error:
        """Last exception encountered."""
        return self._first_last(0)

    @staticmethod
    def _query_types(
        to_search: Dict[int, snowmobile_errors],
        of_type: Optional[snowmobile_errors, List[snowmobile_errors]] = None,
    ) -> Set[int]:
        """Search through exceptions by type."""
        of_type = of_type if isinstance(of_type, Iterable) else [of_type]
        return {
            e for e in to_search if any(isinstance(to_search[e], t) for t in of_type)
        }

    @staticmethod
    def _query_mode(
        to_search: Dict[int, snowmobile_errors], to_raise: bool
    ) -> Set[int]:
        """Search through exceptions by mode (to_raise=True/False)."""

        def _raise(e: Any):
            """Generalized check of an assertion's intention to be raised."""
            return getattr(e, "to_raise") if hasattr(e, "to_raise") else True

        return {
            _id
            for _id, e in to_search.items()
            if (_raise(e) if to_raise else not _raise(e))
        }

    def _query(
        self,
        of_type: Optional[snowmobile_errors, List[snowmobile_errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        from_ctx: Optional[int] = None,
        all_time: bool = False,
    ) -> Dict[int, snowmobile_errors]:
        """Search through exceptions encountered by criterion."""
        to_consider: Dict[int, snowmobile_errors] = (
            self.by_ctx[from_ctx or self.ctx_id] if not all_time else self.by_tmstmp
        )
        seen = set(to_consider)

        if of_type:
            seen = seen.intersection(
                self._query_types(to_search=to_consider, of_type=of_type)
            )

        if isinstance(to_raise, bool):
            seen = seen.intersection(
                self._query_mode(to_search=to_consider, to_raise=to_raise)
            )

        if with_ids:
            seen = seen.intersection(
                set(with_ids if isinstance(with_ids, Iterable) else [with_ids])
            )

        return {i: to_consider[i] for i in sorted(seen, reverse=True)} if seen else {}

    def seen(
        self,
        from_ctx: Optional[int] = None,
        of_type: Optional[Any[snowmobile_errors], List[snowmobile_errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        all_time: bool = False,
    ) -> bool:
        """Boolean indicator of if an exception has been seen."""
        return bool(
            self._query(
                of_type=of_type,
                to_raise=to_raise,
                with_ids=with_ids,
                from_ctx=from_ctx,
                all_time=all_time,
            )
        )

    def get(
        self,
        from_ctx: Optional[int] = None,
        of_type: Optional[Any[snowmobile_errors], List[snowmobile_errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        all_time: bool = False,
        last: bool = False,
        first: bool = False,
        _raise: bool = False,
    ):
        """Boolean indicator of if an exception has been seen."""
        encountered = self._query(
            of_type=of_type,
            to_raise=to_raise,
            with_ids=with_ids,
            from_ctx=from_ctx,
            all_time=all_time,
        )
        if last and not encountered:
            raise InternalError(
                nm="ExceptionHandler.get()",
                msg=f"""
a call was made to `.get()` that returned no exceptions;
exceptions in current context are:\n\t{list(self.current.values())}
""".strip(
                    "\n"
                ),
            )

        if (last or first) and encountered:
            return encountered[list(encountered)[0 if last else -1]]
        return encountered

    @property
    def by_tmstmp(self):
        """All exceptions by timestamp, ordered by most to least recent."""
        unordered = {k2: v2 for k, v in self.by_ctx.items() for k2, v2 in v.items()}
        return {k: unordered[k] for k in sorted(unordered, reverse=True)}

    def __len__(self):
        return len(self.by_tmstmp)

    def __bool__(self):
        """False=no exceptions to be raised in current context."""
        return self.seen(to_raise=True)

    def __repr__(self):
        return (
            f"ExceptionHandler(within={self.within}, contexts={len(self.by_ctx)}, "
            f"cnt={len(self)}, to_raise: {bool(self)}"
        )
