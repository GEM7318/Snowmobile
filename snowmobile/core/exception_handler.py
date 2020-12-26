"""
Module contains the object model for **snowmobile.toml**.
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional, Any, Set, Iterable, Type, Union

from snowmobile.core.errors import InternalError, Error
# from snowmobile.core.script import (
#     StatementNotFoundError,
# )

errors = Union[Error, InternalError]


class ExceptionHandler:
    """Context management for snowmobile objects."""
    def __init__(
            self,
            within: Optional[Any] = None,
            ctx_id: Optional[int] = None,
            in_context: bool = False,
    ):
        self.within = type(within) if within else None
        self.ctx_id: Optional[int] = ctx_id
        self.by_ctx: Dict[int, Dict[int, errors]] = dict()
        self.in_context: bool = in_context
        self.outcome: Optional[int] = None

    def set(
        self, ctx_id: Optional[int] = None, in_context: bool = False,
        outcome: Optional[int] = None,
    ):
        """**Set** attributes on self."""
        if ctx_id:
            if ctx_id in self.by_ctx:
                raise InternalError(
                    nm='ExceptionHandler.set()',
                    msg=f'an existing `ctx_id` was provided to `set(ctx_id)`'
                )
            # ctx_id = ctx_id if ctx_id != -1 else time.time_ns()
            self.ctx_id = ctx_id if ctx_id != -1 else time.time_ns()
            self.by_ctx[self.ctx_id] = {}
        if in_context:
            self.in_context = in_context
        if outcome:
            self.outcome = outcome
        return self

    def reset(
        self, ctx_id: bool = False, in_context: bool = False, outcome: bool = False,
    ):
        """**Reset** attributes on self."""
        if ctx_id:
            self.ctx_id = None
        if in_context:
            self.in_context = False
        if outcome:
            self.outcome = None
        return self

    @property
    def current(self):
        """All exceptions in the current context."""
        if not self.ctx_id:
            raise InternalError(
                nm='ExceptionalHandler.current',
                msg=f"""
A call was made to `.current` while the current value of 'ctx_id` is None.                 
""".strip('\n')
            )
        return self.by_ctx[self.ctx_id] if self.ctx_id in self.by_ctx else {}

    def collect(self, e: Any[errors]):
        """Stores an exception."""
        # self.current[int(time.time_ns())] = e
        # return self

        current = self.current
        current[int(time.time_ns())] = e
        self.by_ctx[self.ctx_id] = current

    def _first_last(self, idx: int):
        """Last exception encountered."""
        by_tmstmp = self.by_tmstmp
        return by_tmstmp[list(by_tmstmp)[idx]]

    @property
    def first(self):
        """First exception encountered."""
        return self._first_last(-1)

    @property
    def last(self):
        """Last exception encountered."""
        return self._first_last(0)

    def _query(
        self,
        of_type: Optional[errors, List[errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        from_ctx: Optional[int] = None,
        all_time: bool = False,
    ) -> Dict[int, errors]:
        """Search through exceptions encountered by criterion."""
        to_consider: Dict[int, errors] = (
            self.by_ctx[from_ctx or self.ctx_id]
            if not all_time
            else self.by_tmstmp
        )
        seen = set(to_consider)
        if of_type:
            of_type = of_type if isinstance(of_type, Iterable) else [of_type]
            matching_type = {
                e: any(isinstance(to_consider[e], t) for t in of_type)
                for e in to_consider
            }
            seen = seen.intersection({e for e, m in matching_type.items() if m})
        if isinstance(to_raise, bool):
            _to_raise = {
                _id for _id, e in to_consider.items()
                if (e.to_raise if to_raise else not e.to_raise)
            }
            seen = seen.intersection(_to_raise)
        if with_ids:
            ids = set(with_ids if isinstance(with_ids, Iterable) else [with_ids])
            seen = seen.intersection(ids)
        return (
            {i: to_consider[i] for i in sorted(seen, reverse=True)}
            if seen
            else {}
        )

    def seen(
        self,
        from_ctx: Optional[int] = None,
        of_type: Optional[Any[errors], List[errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        all_time: bool = False,
    ) -> bool:
        """Boolean indicator of if an exception has been seen."""
        return bool(
            self._query(
                of_type=of_type, to_raise=to_raise, with_ids=with_ids,
                from_ctx=from_ctx, all_time=all_time
            )
        )

    def get(
        self,
        from_ctx: Optional[int] = None,
        of_type: Optional[Any[errors], List[errors]] = None,
        to_raise: Optional[bool] = None,
        with_ids: Optional[int, List[int], Set[int]] = None,
        all_time: bool = False,
        last: bool = False,
        first: bool = False,
        _raise: bool = False,
    ):
        """Boolean indicator of if an exception has been seen."""
        encountered = self._query(
            of_type=of_type, to_raise=to_raise, with_ids=with_ids,
            from_ctx=from_ctx, all_time=all_time
        )
        if last and not encountered:
            raise InternalError(
                nm="ExceptionHandler.get()",
                msg=f"""
a call was made to `.get()` that returned no exceptions;
exceptions in current context are:\n\t{list(self.current.values())}
""".strip('\n')
            )

        if (last or first) and encountered:
            return encountered[list(encountered)[0 if last else -1]]
        return encountered

    @property
    def by_tmstmp(self):
        """All exceptions by timestamp, ordered by most to least recent."""
        unordered = {
            k2: v2
            for k, v in self.by_ctx.items()
            for k2, v2 in v.items()
        }
        return {k: unordered[k] for k in sorted(unordered, reverse=True)}

    def __setattr__(self, key, value):
        vars(self)[key] = value
