"""Tests for :class:`snowmobile.Script` functionality."""
import pytest

import snowmobile


@pytest.mark.script
def test_script_depth(sql_paths, sn_delayed):
    """Tests the standard depth of a script."""
    # given
    script = snowmobile.Script(
        path=sql_paths['generic_script.sql'],
        sn=sn_delayed
    )
    # then
    assert script.depth == 7
