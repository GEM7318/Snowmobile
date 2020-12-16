"""Test loader"""
import pytest


@pytest.mark.loading
def test_loader():
    """Temporary - verify the most basic operations of a loader object."""
    import snowmobile
    table_name = 'test_snowmobile_upload'
    sn1 = snowmobile.Connector(creds='gem7318')
    df = sn1.query('select * from dsc.align_dim_v1 limit 10')
    table = snowmobile.Loader(
        df=df,
        table=table_name,
        sn=sn1,
    )
    loaded = table.load()
    assert loaded
