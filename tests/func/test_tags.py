"""
Tests for tag parsing.
"""
import pytest

from tests import script as get_script


# noinspection PyProtectedMember
def _setup_for_test_tag_from_stripped_line():
    """Gets test cases and generates IDs for statement tags."""
    # get script with tag test cases
    script = get_script(script_name='no_tags.sql')

    # remove index from generated tag
    for s in script._statements_all.values():
        s.tag.incl_idx_in_desc = False

    # generate test cases
    test_cases = [
        (s.tag.nm_ge, s.tag.nm_pr)
        for s in script.statements.values()
    ]

    # generate IDs test cases/console output
    ids = [
        f"FirstLine='{s.tag.first_line}',Tag='{s.tag.nm}'"
        for s in script.statements.values()
    ]

    return ids, test_cases


ids, test_cases = _setup_for_test_tag_from_stripped_line()


@pytest.mark.tags
@pytest.mark.parametrize(
    "tags", test_cases, ids=ids,
)
def test_tag_from_stripped_line(sn, tags):
    """Testing tag generation from sql statements in no_tags.sql."""
    tag_generated, tag_expected = tags
    assert tag_generated == tag_expected
