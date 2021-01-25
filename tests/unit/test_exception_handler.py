"""
Unit tests for :class:`ExceptionHandler`.
"""

import pytest

import time
from typing import Union

from snowmobile.core.errors import (
    StatementNotFoundError,
    DuplicateTagError,
    QAFailure,
    QAEmptyFailure,
    QADiffFailure,
    InternalError,
    Error,
)

errors = Union[
    StatementNotFoundError,
    DuplicateTagError,
    QAFailure,
    QAEmptyFailure,
    QADiffFailure,
    InternalError,
    Error,
]


@pytest.mark.exception_handler
def test_default_exception_handler_defaults(default_test_exception_handler):
    """Testing default values of ExceptionHandler object."""
    assert default_test_exception_handler.within is None
    assert isinstance(default_test_exception_handler.ctx_id, int)
    assert default_test_exception_handler.by_ctx
    assert not default_test_exception_handler.in_context
    assert default_test_exception_handler.outcome is None


@pytest.mark.exception_handler
def test_exception_handler_core(
    snowmobile_test_exception_handler,
    sn_delayed,
    any_unique_integer1,
    any_unique_integer2,
    any_exception_marked_not_to_be_raised1,
    any_exception_marked_not_to_be_raised2,
    to_be_raised_exception1,
    to_be_raised_exception2,
):
    """Kitchen sink testing of ExceptionHandler functionality.."""
    e = snowmobile_test_exception_handler

    any_dormant_exc1, typ_exc_d1 = any_exception_marked_not_to_be_raised1
    any_dormant_exc2, typ_exc_d2 = any_exception_marked_not_to_be_raised2
    any_raise_exc1, typ_exc_r1 = to_be_raised_exception1
    any_raise_exc2, typ_exc_r2 = to_be_raised_exception2

    assert e.within == type(sn_delayed)  # expected: snowmobile.Snowmobile

    def with_one_dormant_exception():
        """setting an initial `ctx_id`; collecting a dormant exception."""
        # -- setting e.ctx_id #1 --
        e.set(ctx_id=any_unique_integer1)
        assert e.ctx_id == any_unique_integer1

        # -- collect exception1 --
        e.collect(e=any_dormant_exc1)

        assert isinstance(e.last, typ_exc_d1)
        assert e.last == e.first

        assert e.seen(of_type=typ_exc_d1) == e.seen(of_type=[typ_exc_d1])

    def with_another_dormant_exception():
        """Collecting another dormant exception."""
        # -- collect exception2 --
        time.sleep(1)
        e.collect(e=any_dormant_exc2)

        assert e.get() == e.current == e.by_tmstmp

        assert isinstance(e.first, typ_exc_d1)
        assert isinstance(e.last, typ_exc_d2)
        assert e.last != e.first

        assert e.get(to_raise=True) == dict()
        assert not e.seen(to_raise=True)

    def with_an_additional_exception_to_be_raised():
        """Collecting an exception **to be raised**."""
        # -- collect exception3; FIRST TO BE RAISED --
        time.sleep(1)
        e.collect(e=any_raise_exc1)

        assert len(e.get()) == 3
        assert len(e.get(to_raise=True)) == 1
        assert e.get(to_raise=True, first=True) == e.get(to_raise=True, last=True)

        assert e.seen(to_raise=True, of_type=typ_exc_r1)
        assert not e.seen(to_raise=True, of_type=typ_exc_d1)

    def with_a_new_ctx_id_and_an_exception_to_be_raised():
        """Setting a new `ctx_id` and collecting an exception to **be raised**."""
        # -- set ctx_id --
        e.set(ctx_id=any_unique_integer2)

        assert e.ctx_id == any_unique_integer2

        assert e.seen(from_ctx=any_unique_integer1)
        assert not e.seen(from_ctx=any_unique_integer2)

        # -- collect exception4; first in current context --
        assert not e.seen(to_raise=True)
        e.collect(e=any_raise_exc2)
        assert e.seen(to_raise=True)

        assert e.get(to_raise=True, first=True) == e.get(to_raise=True, last=True)
        assert not e.seen(to_raise=False)

    def core_exception_querying_across_two_ctx_ids():
        """Test core behavior of querying exception information from two separate
        `ctx_id`(s)."""
        assert len(e.by_ctx) == 2

        assert len(e.get(from_ctx=any_unique_integer1)) == 3
        assert len(e.get(from_ctx=any_unique_integer1, to_raise=True)) == 1
        assert len(e.get(from_ctx=any_unique_integer1, to_raise=False)) == 2

        assert len(e.get(from_ctx=any_unique_integer2)) == 1
        assert len(e.get(from_ctx=any_unique_integer2, to_raise=True)) == 1
        assert len(e.get(from_ctx=any_unique_integer2, to_raise=False)) == 0

    with_one_dormant_exception()
    with_another_dormant_exception()
    with_an_additional_exception_to_be_raised()
    with_a_new_ctx_id_and_an_exception_to_be_raised()
    core_exception_querying_across_two_ctx_ids()
