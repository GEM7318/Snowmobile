"""Tests for :class:`snowmobile.Script` functionality."""
import pytest

import snowmobile

from tests import FILES


@pytest.mark.script
def test_script_depth(sn_delayed):
    """Tests the standard depth of a script."""
    # given
    script = snowmobile.Script(
        path=FILES['generic_script.sql'],
        sn=sn_delayed
    )
    # then
    assert script.depth == 7
