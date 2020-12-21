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


@pytest.fixture()
def a_sample_tag(sn):
    """Testing __setattr__ on Tag.."""
    from snowmobile.core.statement.tag import Tag

    # noinspection SqlResolve
    return Tag(
        configuration=sn.cfg,
        nm_pr='test-tag',
        first_keyword='select',
        sql='select * from sample_table',
        index=1,
    )


def test_set_item_on_tag(a_sample_tag):
    """Testing __setattr__ and __bool__ on Tag.."""
    a_sample_tag.is_included = False
    a_sample_tag.__setitem__('is_included', False)
    assert not a_sample_tag.is_included
    assert not a_sample_tag


def test_repr_on_tag(a_sample_tag):
    """Testing __repr__ on Tag.."""
    assert a_sample_tag.__repr__() == "statement.Tag(nm='test-tag')"
