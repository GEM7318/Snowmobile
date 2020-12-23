"""Tests for :class:`snowmobile.Script` functionality."""
import pytest

from tests import (
    FILES,
)

QA_SCRIPT_NAME = 'tags_qa_statements.sql'

# TODO: Docstrings/comments


@pytest.fixture(scope='session')
def setup_for_qa_statement_tests(sn):
    """Sets up script and temp table for QA statement tests."""
    from snowmobile import Script
    script = Script(
        path=FILES[QA_SCRIPT_NAME],
        sn=sn
    )
    script.run(1)  # create temp table for statements to run on
    return script


@pytest.mark.qa
def test_qa_empty_passes(setup_for_qa_statement_tests):
    """Verifies that a valid `qa-empty` passes validation and contains correct attributes.
    """
    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-empty'], incl_desc=['.*expected pass']
    ) as s:
        s.run()                                  # run w/ default error handling
        for s2 in s.executed.values():
            assert s2.outcome                    # outcome bool
            assert s2.outcome_txt() == 'passed'  # outcome text
            assert not s2.errors                 # no errors encountered


@pytest.mark.qa
def test_qa_diff_passes(setup_for_qa_statement_tests):
    """Verifies that a valid `qa-empty` throws no exception and contains the
    correct attributes.
    """
    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-diff'], incl_desc=['.*expected pass']
    ) as s:
        s.run()                                  # run w/ default error handling
        for s2 in s.executed.values():
            assert s2.outcome                    # outcome bool
            assert s2.outcome_txt() == 'passed'  # outcome text
            assert not s2.errors                 # no errors encountered


@pytest.mark.qa
def test_qa_empty_failures(setup_for_qa_statement_tests):
    """Verifies that a valid `qa-empty` throws no exception and contains the
    correct attributes.
    """
    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-empty'], incl_desc=['.*expected failure']
    ) as s:
        s.run(on_failure='c')                    # SILENCING QA FAILURES
        for s2 in s.executed.values():           # ..note: Exception tests below
            assert not s2.outcome                # NOT outcome bool
            assert s2.outcome_txt() == 'failed'  # 'failed' outcome text
            assert s2.errors                     # errors encountered


@pytest.mark.qa
def test_qa_diff_failures(setup_for_qa_statement_tests):
    """Verifies that a valid `qa-empty` throws no exception and contains the
    correct attributes.
    """
    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-diff'], incl_desc=['.*expected failure']
    ) as s:
        s.run(on_failure='c')                    # !! SILENCING QA FAILURES !!
        for s2 in s.executed.values():
            assert s2.outcome                    # NOT outcome bool
            assert s2.outcome_txt() == 'failed'  # 'failed' outcome text
            assert s2.errors                 # no errors encountered


@pytest.mark.exceptions
@pytest.mark.qa
def test_qa_empty_failure_exceptions(setup_for_qa_statement_tests):
    """Verifies that an invalid `qa-empty` throws appropriate exception."""
    from snowmobile.core.statement import QAEmptyFailure

    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-empty'], incl_desc=['.*expected failure']
    ) as s:

        with pytest.raises(QAEmptyFailure):
            s.run()         # verify with `script.run()`
        for i in s.statements:
            with pytest.raises(QAEmptyFailure):
                s.run(i)    # verify same when calling `script.run()` on each statement
            with pytest.raises(QAEmptyFailure):
                s(i).run()  # verify with each statement's `.run()` method


@pytest.mark.exceptions
@pytest.mark.qa
def test_qa_diff_failure_exceptions(setup_for_qa_statement_tests):
    """Verifies that an invalid `qa-diff` throws appropriate exception."""
    from snowmobile.core.statement import QADiffFailure
    script = setup_for_qa_statement_tests
    with script.filter(
        incl_anchor=['qa-diff'], incl_desc=['.*expected failure']
    ) as s:
        with pytest.raises(QADiffFailure):
            s.run()

        for i in s.statements:
            with pytest.raises(QADiffFailure):
                s.run(i)
            with pytest.raises(QADiffFailure):
                s(i).run()


@pytest.mark.exceptions
@pytest.mark.qa
def test_qa_diff_post_processing_exception(setup_for_qa_statement_tests):
    """Verifies that an invalid `qa-diff` throws appropriate exception."""
    from snowmobile.core.statement.errors import StatementPostProcessingError

    script = setup_for_qa_statement_tests

    with script.filter(incl_nm=['verify an exception is thrown']) as s:

        with pytest.raises(StatementPostProcessingError):
            s.run()

        for i in s.statements:
            with pytest.raises(StatementPostProcessingError):
                s.run(i)

            with pytest.raises(StatementPostProcessingError):
                s(i).run()
