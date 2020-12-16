# -*- coding: utf-8 -*-

import pytest
collect_ignore = ["__init__.py", "pkg_data", "_stdout.py"]


@pytest.fixture()
def sn():
    """Returns a standard `Connector` object."""
    import snowmobile
    return snowmobile.Connector(config_file_nm='snowmobile_testing.toml')


@pytest.fixture()
def sn_delayed():
    """Returns a delayed `Connector` object."""
    import snowmobile
    return snowmobile.Connector(
        config_file_nm='snowmobile_testing.toml', delay=True
    )


@pytest.fixture()
def sql_paths():
    """Returns a dictionary of all sql file names to associated Path(s)."""
    from pathlib import Path
    sql_dir = (
        Path("/".join(Path.cwd().as_posix().partition("Snowmobile")[:-1]))
        / "tests"
        / "func"
        / "data"
        / "sql"
    )
    scripts = [p for p in sql_dir.rglob('*.sql')]
    return {p.name: p for p in scripts}
