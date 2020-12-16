"""Tests for script __markers__."""
import pytest

import snowmobile


@pytest.mark.markers
def test_marker_number_standard(sn_delayed, sql_paths):
    """Test that 4 distinct markers are identified in `markers_standard.sql`"""
    # given
    script = snowmobile.Script(
        path=sql_paths['markers_standard.sql'],
        sn=sn_delayed
    )
    # then
    assert len(script.markers) == 4


@pytest.mark.markers
def test_marker_number_duplicates(sn_delayed, sql_paths):
    """Test that two distinct markers were identified amongst 3 total in
    `markers_duplicates.sql`."""
    # given
    script = snowmobile.Script(
        path=sql_paths['markers_duplicates.sql'],
        sn=sn_delayed
    )
    # then
    assert len(script.markers) == 2

# TESTS: Add in a test like the below except for different types of Statement
#   objects.


def _get_test_cases_for_combined_marker_and_statement_indices():
    """Get expected values for contents by index."""
    from snowmobile.core import Statement
    from snowmobile.core.configuration.schema import Marker
    return [
        (1, Marker, 'markers_standard.sql'),
        (2, Statement, 'create-table~sample_table'),
        (3, Marker, 'marker2'),
        (4, Marker, 'marker3'),
        (5, Statement, 'create-table~sample_table2'),
        (6, Marker, 'trailing_marker'),
    ]


@pytest.mark.markers
def test_combined_marker_and_statement_indices(sn_delayed, sql_paths):
    """Test that the combined marker and statement order is correct."""
    # given
    script = snowmobile.Script(
        path=sql_paths['markers_standard.sql'],
        sn=sn_delayed
    )
    contents_under_test = script.contents(by_index=True, markers=True)
    expected_contents = _get_test_cases_for_combined_marker_and_statement_indices()
    # then
    for exp, (i, c) in zip(expected_contents, contents_under_test.items()):
        exp_index, exp_base_class, exp_name = exp
        assert exp_index == i
        assert exp_name == c.name
        assert isinstance(c, exp_base_class)
