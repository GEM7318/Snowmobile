# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
collect_ignore = ["__init__.py", "pkg_data", "_stdout.py"]

from tests import (
    CONFIG_FILE_NM,
    CREDS,
)

TESTS_DIR = Path(__file__).absolute().parent


@pytest.fixture(scope='session')
def sn():
    """Returns a standard `Connector` object."""
    import snowmobile
    return snowmobile.Connect(
        creds=CREDS, config_file_nm=CONFIG_FILE_NM
    )


@pytest.fixture(scope='session')
def sn_delayed():
    """Returns a delayed `Connector` object."""
    import snowmobile
    return snowmobile.Connect(
        creds=CREDS, config_file_nm=CONFIG_FILE_NM, delay=True
    )


@pytest.fixture(scope='session')
def sql_paths():
    """Returns a dictionary of all sql file names to associated Path(s)."""
    sql_dir = (
        TESTS_DIR
        / "func"
        / "data"
        / "sql"
    )
    scripts = [p for p in sql_dir.rglob('*.sql')]
    return {p.name: p for p in scripts}


@pytest.fixture(scope='session')
def sql(sn_delayed):
    """Returns a sql object; connection omitted."""
    from snowmobile import SQL
    return SQL(
        sn=sn_delayed,
        auto_run=True
    )
