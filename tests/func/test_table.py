"""Test loader"""
import pytest

from tests import CONFIG_FILE_NM, CREDS

TESTING_TABLE_NAME = 'test_snowmobile_table'


@pytest.fixture(scope='session')
def rnp():
    """Returns numpy reference with the seed set to 9."""
    import numpy as np

    def rnp(s: int = 1):
        """Sets numpy seed and returns library reference."""
        np.random.seed(s)
        return np
    return rnp


@pytest.fixture(scope='session')
def df(rnp):
    """Sets seed and returns a DataFrame to use for tests."""
    import pandas as pd

    return pd.DataFrame(
        {
            'col1': [rnp().random.choice(['spam', 'eggs', 'ham']) for _ in range(24)],
            'col2': [rnp().random.choice(['alpha', 'beta', 'gamma']) for _ in range(24)],
            'col3': [i for i in range(24)],
        }
    )


@pytest.mark.table
def test_table(sn, df):
    """Temporary - verify the most basic operations of a loader object."""
    import snowmobile
    table_name = "test_snowmobile_upload"
    table = snowmobile.Table(df=df, table=table_name, sn=sn)
    loaded = table.load(if_exists="replace")
    assert loaded


@pytest.mark.table
def test_table_core_functionality(sn, df, rnp):
    """Kitchen sink testing of core snowmobile.Table functionality"""
    import snowmobile
    import pandas as pd

    # Ex. 1 -------------------------------------------------------------------

    sn.sql.exists(TESTING_TABLE_NAME)

    t1 = snowmobile.Table(sn=sn, table=TESTING_TABLE_NAME, df=df, as_is=True)
    assert t1.loaded

    # Ex. 11 ------------------------------------------------------------------

    from snowmobile.core.errors import ExistingTableError

    with pytest.raises(ExistingTableError):
        snowmobile.Table(
            sn=sn,
            table=TESTING_TABLE_NAME,
            df=df,
            as_is=True,
            if_exists='fail',
        )

    # Ex. 2 -------------------------------------------------------------------

    df2 = pd.concat([df, df], axis=1)

    from snowmobile.core.errors import ColumnMismatchError

    t2 = snowmobile.Table(sn=sn, table=TESTING_TABLE_NAME, df=df2)

    with pytest.raises(ColumnMismatchError):
        t2.load()

    # Ex. 22
    t2.load(if_exists='replace')
    assert t2.loaded

    # Ex. 3 -------------------------------------------------------------------
    with pytest.raises(ValueError):
        t2.load(if_exists='some_invalid_if_exists_value')
