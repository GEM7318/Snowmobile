"""Tests for script __markers__."""
from typing import Tuple, List, Any
import pytest

import snowmobile

from tests import FILES


@pytest.mark.markers
def test_marker_number_standard(sn_delayed):
    """Test that 4 distinct markers are identified in `markers_standard.sql`"""
    # given
    script = snowmobile.Script(path=FILES["markers_standard.sql"], sn=sn_delayed)
    # then
    assert len(script.markers) == 4


@pytest.mark.markers
def test_marker_number_duplicates(sn_delayed):
    """Test that two distinct markers were identified amongst 3 total in
    `markers_duplicates.sql`."""
    # given
    script = snowmobile.Script(path=FILES["markers_duplicates.sql"], sn=sn_delayed)
    # then
    assert len(script.markers) == 2


# TESTS: Add in a test like the below except for different types of Statement
#   objects.


@pytest.mark.markers
def test_combined_marker_and_statement_indices(sn_delayed):
    """Test that the combined marker and statement order is correct."""
    from snowmobile.core import Statement
    from snowmobile.core.cfg import Marker

    script = snowmobile.Script(path=FILES["markers_standard.sql"], sn=sn_delayed)
    script_contents_expected: List[Tuple[int, Any[Marker, Statement], str]] = [
        # (index, BaseClass, 'tag.nm')
        (1, Marker, "markers_standard.sql"),
        (2, Statement, "create table~sample_table"),
        (3, Marker, "marker2"),
        (4, Marker, "marker3"),
        (5, Statement, "create table~sample_table2"),
        (6, Marker, "trailing_marker"),
    ]

    script_contents_under_test = script.contents(by_index=True, markers=True)

    for expected, (i, c) in zip(
        script_contents_expected, script_contents_under_test.items()
    ):
        expected_index, expected_base_class, expected_name = expected
        assert all(
            [
                expected_index == i,
                expected_name == c.nm,
                isinstance(c, expected_base_class),
            ]
        )
