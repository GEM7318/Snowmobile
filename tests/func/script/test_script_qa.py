"""Tests for :class:`snowmobile.Script` functionality."""
import pytest

from tests.func.fixtures import get_script

# fmt: off
_OUTCOME_MAPPING = {
    1: "failed",
    3: "passed"
}
# fmt: on


def _setup_test_qa_instances():
    """Sets up script and temp table for QA statement tests."""
    # script storing QA test cases --------------------------------------------
    script = get_script(script_name='tags_qa_statements.sql')
    # running setup statement that creates a temp table for QA statements -----
    script.run('create-temp table~sample_table')
    # generating test cases ---------------------------------------------------
    test_cases = (
        # qa-empty: expected pass
        (
            {'incl_anchor': ['qa-empty'], 'incl_desc': ['.*expected pass.*']},
            'passed'
        ),
        # qa-diff: expected pass
        (
            {'incl_anchor': ['qa-diff'], 'incl_desc': ['.*expected pass.*']},
            'passed'
        ),
        # qa-empty: expected failure
        (
            {'incl_anchor': ['qa-empty'], 'incl_desc': ['.*expected failure.*']},
            'failed'
        ),
        # qa-diff: expected failure
        (
            {'incl_anchor': ['qa-diff'], 'incl_desc': ['.*expected failure.*']},
            'failed'
        ),
    )
    # generating IDs for pytest console ---------------------------------------
    ids = [
        f"Anchor='{t[0]['incl_anchor']}',Expected='{t[1]}'"
        for t in test_cases
    ]

    return script, ids, test_cases


script, ids, test_cases = _setup_test_qa_instances()


@pytest.mark.qa
@pytest.mark.parametrize(
    "qa", test_cases, ids=ids
)
def test_qa_statements(qa):
    """Tests that QA statements function as expected."""
    # given
    filters, expected_outcome = qa
    with script.filter(**filters) as sql:
        sql.run()
        # then
        assert all(
            _OUTCOME_MAPPING[s.outcome] == expected_outcome
            for s in sql.executed.values()
        )
