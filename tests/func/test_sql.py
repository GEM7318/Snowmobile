"""Tests for snowmobile.SQL."""
import pytest

from snowmobile.core.sql import SQL

from tests import (
    CONFIG_FILE_NM,
    CREDS,
)


@pytest.mark.sql
def test_defaults(sn_delayed):
    # arrange
    sql = SQL(sn=sn_delayed)
    attrs_expected = {
        'sn': sn_delayed,
        'nm': str(),
        'schema': sn_delayed.cfg.connection.current.schema_name,
        'obj': 'table',
        'auto_run': True,
    }
    attrs_under_test = {
        k: vars(sql)[k]
        for k, v in attrs_expected.items()
    }
    for attr_nm, attr_value in attrs_under_test.items():
        assert attr_value == attrs_expected[attr_nm]

