# -*- coding: utf-8 -*-

import pytest

collect_ignore = ["__init__.py", "pkg_data", "_stdout.py"]

from tests import CONFIG_FILE_NM, CREDS


@pytest.fixture(scope="session")
def sn():
    """Returns a standard `Connector` object."""
    import snowmobile

    sn = snowmobile.connect(creds=CREDS, config_file_nm=CONFIG_FILE_NM)
    sn.ex("create schema TESTING_SNOWMOBILE")
    yield sn
    sn.ex("drop schema TESTING_SNOWMOBILE")


@pytest.fixture(scope="session")
def sn_delayed():
    """Returns a delayed `Connector` object."""
    import snowmobile

    return snowmobile.connect(creds=CREDS, config_file_nm=CONFIG_FILE_NM, delay=True)


@pytest.fixture(scope="session")
def sql(sn_delayed):
    """Returns a sql object; connection omitted."""
    from snowmobile import SQL

    return SQL(sn=sn_delayed, auto_run=True)
