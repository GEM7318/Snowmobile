"""
Tests for snowmobile.statement.Scope.
"""
import pytest


@pytest.fixture()
def sample_scope_object(sn_delayed):
    """An example statement object for testing."""
    from snowmobile.core.scope import Scope

    return Scope(arg="kw", base="select")


@pytest.mark.scope
def test_scope_defaults(sample_scope_object):
    """Tests default values of a scope object."""
    assert sample_scope_object.component == "kw"
    assert sample_scope_object.base == "select"

    assert sample_scope_object.incl_arg == "incl_kw"
    assert sample_scope_object.excl_arg == "excl_kw"

    assert not sample_scope_object.is_excluded
    assert not sample_scope_object.is_included
    assert not sample_scope_object

    assert sample_scope_object.fallback_to == {"incl_kw": ["select"], "excl_kw": []}


@pytest.mark.scope
def test_scope_dunder_methods(sample_scope_object):
    """Tests dunder methods for a scope object."""
    assert repr(sample_scope_object) == "Scope(arg='kw', base='select')"
    assert str(sample_scope_object) == "Scope(arg='kw', base='select', included=False)"
    assert not bool(sample_scope_object)
