"""Tests for snowmobile.Statement."""
import pytest


# noinspection SqlResolve
@pytest.fixture()
def sample_statement_object(sn):
    """An example statement object for testing."""
    from snowmobile import Statement

    # creating an example table
    sn.ex('drop table if exists an_example_table')
    sn.ex('create temp table an_example_table as select 1 as sample_col')

    # sql for statement object
    sql = """
select
    *
from an_example_table a;    
"""
    return Statement(
        sn=sn,
        statement=sn.cfg.script.ensure_sqlparse(sql=sql.strip('\n')),
        index=1
    )


@pytest.mark.statement
def test_statement_number_of_lines(sample_statement_object):
    """Tests the statement.lines property."""
    assert sample_statement_object.lines == 3


@pytest.mark.statement
def test_multiline_attributes_without_a_name_causes_error(sample_statement_object):
    """Verifies that a multiline tag without a '__name:' argument will raise an error."""
    from snowmobile.core.errors import InvalidTagsError

    multiline_tag_without_a_name_argument = """
__description: This is an example of a multiline tag that will cause an error.    
"""

    # given
    sample_statement_object.attrs_raw = multiline_tag_without_a_name_argument
    sample_statement_object.is_multiline = True
    sample_statement_object.is_tagged = True

    # then
    with pytest.raises(InvalidTagsError):
        sample_statement_object.parse()


@pytest.mark.statement
def test_calling_render_on_a_valid_statement_does_not_cause_an_error(sample_statement_object):
    """Tests statement.render() method does not cause an error."""
    sample_statement_object.run(render=True)


# noinspection SqlResolve
@pytest.mark.statement
def test_calling_run_with_results_on_invalid_sql_raises_database_error(sample_statement_object):
    """Tests `s.run(as_df=True)` raises an error when `s.sql` is not a valid statement."""
    from pandas.io.sql import DatabaseError
    # given
    an_invalid_sql_statement = 'select * from *'
    sample_statement_object.sql = an_invalid_sql_statement

    # then
    with pytest.raises(DatabaseError):
        sample_statement_object.run(as_df=True)


@pytest.mark.statement
def test_statement_dunder_getitem(sample_statement_object):
    """Verifies `s.__getitem__()`."""
    assert sample_statement_object.__getitem__(item='sql') == sample_statement_object.sql


@pytest.mark.statement
def test_statement_dunder_str(sample_statement_object):
    """Verifies `s.__str__()`."""
    assert str(sample_statement_object) == "Statement('select data~statement #1')"


@pytest.mark.statement
def test_statement_dunder_setitem(sample_statement_object):
    """Verifies `s.__str__()`."""
    sample_statement_object.__setitem__('sql', '')
    assert sample_statement_object.sql == ''
