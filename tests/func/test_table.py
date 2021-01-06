"""Test loader"""
import pytest

from tests import CONFIG_FILE_NM, CREDS


@pytest.mark.table
def test_table(sn):
    """Temporary - verify the most basic operations of a loader object."""
    import snowmobile

    table_name = "test_snowmobile_upload"
    df = sn.query("select 1 as sample_column")
    table = snowmobile.Table(df=df, table=table_name, sn=sn)
    loaded = table.load(if_exists="replace")
    assert loaded
