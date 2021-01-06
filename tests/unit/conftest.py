"""
Unit tests for :class:`ExceptionHandler`.
"""

import pytest

import time
from typing import Union, Tuple, Type

from snowmobile.core.exception_handler import ExceptionHandler

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


@pytest.fixture(scope="session")
def default_test_exception_handler() -> ExceptionHandler:
    """ExceptionHandler with completely default values."""
    return ExceptionHandler()


@pytest.fixture(scope="session")
def snowmobile_test_exception_handler(sn_delayed) -> ExceptionHandler:
    """ExceptionHandler with completely default values."""
    from snowmobile.core.exception_handler import ExceptionHandler

    return ExceptionHandler(within=sn_delayed)


@pytest.fixture(scope="session")
def any_exception_marked_not_to_be_raised1() -> Tuple[errors, Type[errors]]:
    """sample1"""
    e = InternalError(nm="1st example exception", msg="testing 1st")
    return e, InternalError


@pytest.fixture(scope="session")
def any_exception_marked_not_to_be_raised2() -> Tuple[errors, Type[errors]]:
    """sample2"""
    e = StatementNotFoundError(nm="2nd example exception", msg="testing 2nd")
    return e, StatementNotFoundError


@pytest.fixture(scope="session")
def to_be_raised_exception1() -> Tuple[errors, Type[errors]]:
    """FIRST SAMPLE EXCEPTION MARKED AS TO BE RAISED."""
    e = DuplicateTagError(nm="3rd example exception", msg="testing 3rd", to_raise=True)
    return e, DuplicateTagError


@pytest.fixture(scope="session")
def to_be_raised_exception2() -> Tuple[errors, Type[errors]]:
    """SECOND SAMPLE EXCEPTION MARKED AS TO BE RAISED."""
    e = QAFailure(nm="4th example exception", msg="testing 4th", to_raise=True, idx=0)
    return e, QAFailure


@pytest.fixture(scope="session")
def any_unique_integer1() -> int:
    """To be used as `ctx_id` #1."""
    return time.time_ns()


@pytest.fixture(scope="session")
def any_unique_integer2() -> int:
    """To be used as `ctx_id` #2."""
    time.sleep(1)
    return time.time_ns()
