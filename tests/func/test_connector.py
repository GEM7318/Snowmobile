"""Tests for snowmobile.Connect()."""
import pytest

import snowmobile

from tests import (
    CONFIG_FILE_NM,
    CREDS,
)


@pytest.mark.connector
def test_basic_query(sn):
    """Verify a standard connector object connects to the DB."""
    df = sn.query("select 1")
    assert not df.empty, "expected df.empty=False"


@pytest.mark.connector
def test_basic_query_via_ex(sn):
    """Verify a standard connector object connects to the DB."""
    cur = sn.ex("select 1")
    assert cur.fetchone()[0] == 1


@pytest.mark.connector
def test_providing_results_equal_false_returns_cursor_not_a_df(sn):
    """Verifies passing `results=False` to connector.query() returns a cursor."""
    from snowflake.connector.connection import SnowflakeCursor
    cur = sn.query("select 1", results=False)
    assert isinstance(cur, SnowflakeCursor)


@pytest.mark.connector
def test_alive_evaluates_to_false_on_delayed_connection(sn_delayed):
    """Verify a delayed connector object does not connect to the DB."""
    assert not sn_delayed.alive


@pytest.mark.connector
def test_cursor_is_accessible_from_delayed_connection(sn_delayed):
    """Verify a delayed connector object does not connect to the DB."""
    assert not sn_delayed.cursor.is_closed()


@pytest.mark.connector
def test_alive_evaluates_to_false_post_disconnect(sn):
    """Verifies connector.disconnect() closes session."""
    assert not sn.disconnect().alive, "expected sn_delayed.alive=False post-disconnect"


# noinspection PyUnresolvedReferences
@pytest.mark.connector
def test_alternate_kwarg_takes_precedent_over_configuration_file():
    """Tests over-riding configuration file with alternate connection kwargs."""
    sn_as_from_config = snowmobile.Connect(
        creds=CREDS,
        config_file_nm=CONFIG_FILE_NM
    )
    sn_with_a_conflicting_parameter = snowmobile.Connect(
        creds=CREDS,
        config_file_nm=CONFIG_FILE_NM,
        autocommit=False  # <-- explicit kwarg that also exists in snowmobile.toml
    )

    assert (
        # verify `config.autocommit=True`
        sn_as_from_config.conn._autocommit

        # verify `autocommit=False` kwarg took precedent over config
        and not sn_with_a_conflicting_parameter.conn._autocommit
    )


@pytest.mark.connector
def test_providing_invalid_credentials_raises_exception(sn):
    """Verify an invalid set of credentials raises DatabaseError."""
    from snowflake.connector.errors import DatabaseError
    with pytest.raises(DatabaseError):
        snowmobile.Connect(
            creds=CREDS,
            config_file_nm=CONFIG_FILE_NM,
            user='invalid@invalid.com'  # <-- a set of invalid credentials
        )


# noinspection SqlResolve
@pytest.mark.connector
def test_invalid_sql_passed_to_query_raises_exception(sn):
    """Tests that invalid sql passed to connector.query() raises DatabaseError."""
    from pandas.io.sql import DatabaseError
    with pytest.raises(DatabaseError):
        sn.query('select * from *')  # <-- an invalid sql statement


# noinspection SqlResolve
@pytest.mark.connector
def test_invalid_sql_passed_to_ex_raises_exception(sn):
    """Tests that invalid sql passed to connector.ex() raises ProgrammingError."""
    from snowflake.connector.errors import ProgrammingError
    with pytest.raises(ProgrammingError):
        sn.ex('select * from *')  # <-- an invalid sql statement


@pytest.mark.connector
def test_dunder_repr_is_valid(sn):
    assert sn.__repr__()