"""Test connector."""

import pytest


@pytest.mark.connector
def test_connector(sn):
    """Verify a standard connector object connects to the DB."""
    df = sn.query("select 1")
    assert not df.empty


@pytest.mark.connector
def test_delayed_connection(sn_delayed):
    """Verify a delayed connector object does not connect to the DB."""
    assert not sn_delayed.alive

