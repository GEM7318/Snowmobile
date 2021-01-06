"""Tests for :class:`snowmobile.Script` functionality."""
import pytest

import snowmobile

from tests import FILES

ANY_SCRIPT_NAME = "tags_qa_statements.sql"


@pytest.mark.script
def test_providing_invalid_path_raises_correct_exception(
    sn_delayed, any_invalid_file_path
):
    """Verifies providing an invalid `path` argument raises FileNotFoundError."""
    from snowmobile import Script

    with pytest.raises(FileNotFoundError):
        _ = Script(sn=sn_delayed, path=any_invalid_file_path)


# noinspection SqlResolve
@pytest.mark.script
def test_using_from_str_instantiation(sn_delayed):
    """Tests snowmobile.Script().from_str() instantiation."""
    from snowmobile import Script

    ANY_PIECE_OF_SQL = "select * from any_table"
    ANY_VALID_DIRECTORY = FILES[ANY_SCRIPT_NAME].parent
    ANY_FILE_NAME_WITHOUT_A_SQL_EXT = "any-file.json"  # sourcery skip: move-assign

    script = Script(sn=sn_delayed).from_str(  # given 1
        sql=ANY_PIECE_OF_SQL, name=ANY_SCRIPT_NAME, directory=ANY_VALID_DIRECTORY
    )
    assert script.source == ANY_PIECE_OF_SQL  # then 1.1
    assert script.path == ANY_VALID_DIRECTORY / ANY_SCRIPT_NAME  # then 1.2

    with pytest.raises(ValueError):  # then 2.1
        _ = Script(sn=sn_delayed).from_str(  # given 2
            sql=ANY_PIECE_OF_SQL,
            name=ANY_FILE_NAME_WITHOUT_A_SQL_EXT,  # <-- cause of exception
            directory=ANY_VALID_DIRECTORY,
        )


@pytest.mark.script
def test_script_depth(sn_delayed):
    """Tests the standard depth of a script."""
    # given
    script = snowmobile.Script(path=FILES["generic_script.sql"], sn=sn_delayed)
    # then
    assert script.depth == 7
