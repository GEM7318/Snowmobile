"""Test loader"""
import pytest


@pytest.mark.loading
def test_loader():
    """Temporary - verify the most basic operations of a loader object."""
    import snowmobile
    table_name = 'test_snowmobile_upload'
    sn1 = snowmobile.Connector(creds='snowmobile_testing')
    df = sn1.query('select * 1 as sample_column')
    table = snowmobile.Loader(
        df=df,
        table=table_name,
        sn=sn1,
    )
    loaded = table.load()
    assert loaded
