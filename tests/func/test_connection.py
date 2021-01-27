"""Tests for snowmobile.Snowmobile."""
import pytest

import snowmobile

from tests import CONFIG_FILE_NM, CREDS


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
def test_query_into_cursor(sn):
    """Verifies passing `as_cur=True` to snowmobile.query() returns a cursor."""
    from snowflake.connector.connection import SnowflakeCursor

    cur = sn.query("select 1", as_cur=True)
    assert isinstance(cur, SnowflakeCursor)


@pytest.mark.connector
def test_query_into_dictcursor(sn):
    """Verifies passing `as_dcur=True` to snowmobile.query() returns a dictcursor."""
    from snowflake.connector import DictCursor

    dcur = sn.query("select 1", as_dcur=True)
    assert isinstance(dcur, DictCursor)


@pytest.mark.connector
def test_query_as_scalar(sn):
    """Verifies passing `as_dcur=True` to snowmobile.query() returns a dictcursor."""
    scalar = sn.query("select 1", as_scalar=True)
    assert scalar == 1


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
    sn_as_from_config = snowmobile.connect(creds=CREDS, config_file_nm=CONFIG_FILE_NM)
    sn_with_a_conflicting_parameter = snowmobile.connect(
        creds=CREDS,
        config_file_nm=CONFIG_FILE_NM,
        autocommit=False,  # <-- explicit kwarg that also exists in snowmobile.toml
    )

    assert (
        # verify `config.autocommit=True`
        sn_as_from_config.con._autocommit
        # verify `autocommit=False` kwarg took precedent over config
        and not sn_with_a_conflicting_parameter.con._autocommit
    )


@pytest.mark.connector
def test_providing_invalid_credentials_raises_exception(sn):
    """Verify an invalid set of credentials raises DatabaseError."""
    from snowflake.connector.errors import DatabaseError

    with pytest.raises(DatabaseError):
        snowmobile.connect(
            creds=CREDS,
            config_file_nm=CONFIG_FILE_NM,
            user="invalid@invalid.com",  # <-- a set of invalid credentials
        )


# noinspection SqlResolve
@pytest.mark.connector
def test_invalid_sql_passed_to_query_raises_exception(sn):
    """Tests that invalid sql passed to snowmobile.query() raises DatabaseError."""
    from pandas.io.sql import DatabaseError

    with pytest.raises(DatabaseError):
        sn.query("select * from *")  # <-- an invalid sql statement


# noinspection SqlResolve
@pytest.mark.connector
def test_invalid_sql_passed_to_ex_raises_exception(sn):
    """Tests that invalid sql passed to connector.ex() raises ProgrammingError."""
    from snowflake.connector.errors import ProgrammingError

    with pytest.raises(ProgrammingError):
        sn.ex("select * from *")  # <-- an invalid sql statement


# noinspection SqlResolve
@pytest.mark.connector
def test_invalid_sql_passed_to_exd_raises_exception(sn):
    """Tests that invalid sql passed to connector.ex() raises ProgrammingError."""
    from snowflake.connector.errors import ProgrammingError

    with pytest.raises(ProgrammingError):
        sn.exd("select * from *")  # <-- an invalid sql statement


@pytest.mark.connector
def test_invalid_credentials_alias_raises_exception():
    """Tests that an invalid credentials name creds raises KeyError."""
    from snowmobile import Snowmobile

    with pytest.raises(KeyError):
        Snowmobile(creds="name_for_a_nonexistent_set_of_creds")


@pytest.mark.connector
def test_masked_dunder_str_method_for_sets_of_credentials(sn):
    """Verifies that the __str()__ method for a set of credentials is masked."""
    assert all(
        not line.split("=")[-1].strip("'").replace("*", "")
        for line in str(sn.cfg.connection.credentials).split("\n")
        if str(line).startswith("  ")
    )


@pytest.mark.connector
def test_dunder_repr_is_valid(sn):
    assert sn.__repr__()


@pytest.mark.connector
def test_invalid_arguments_provided_to_query_raises_value_error(sn):
    """Verifies an error gets thrown if two return types are specified."""
    with pytest.raises(ValueError):
        sn.query('select 1', as_df=True, as_dcur=True)
