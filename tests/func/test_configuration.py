"""Test connector."""

from typing import Tuple

import pytest

from tests import CONFIG_FILE_NM

from snowmobile import Connector

CACHE_TESTING_ITEM_NAME1 = "test-path"
CACHE_TESTING_ITEM_NAME2 = "test-path2"


@pytest.fixture(scope="module")
def cache_with_a_testing_value_saved(sn_delayed) -> Tuple[Connector, str]:
    """Performs setup for cache testing.

    Specifically:
        *   Uses current configuration file location as the (str) value to cache
        *   Ensures the name of the item to cache isn't already cached
        *   Saves a test item to the cache
        *   Returns the modified connector object and the value that was cached

    """
    # use current config file location as the value to cache
    value_to_cache = sn_delayed.cfg.location.as_posix()

    # ensure 'test-path' is not currently a cached value
    if sn_delayed.cfg.cache.get(CACHE_TESTING_ITEM_NAME1):
        sn_delayed.cfg.cache.clear(CACHE_TESTING_ITEM_NAME1)

    # save two values to cache under the testing item names
    for name in [CACHE_TESTING_ITEM_NAME1, CACHE_TESTING_ITEM_NAME2]:
        sn_delayed.cfg.cache.save_item(item_name=name, item_value=value_to_cache)

    return sn_delayed, value_to_cache


@pytest.mark.cache
@pytest.mark.configuration
def test_cache_save(cache_with_a_testing_value_saved):
    """Tests that the value cached matches the string value retrieved based on its name."""
    sn_delayed, cached_value = cache_with_a_testing_value_saved

    test_value_from_cache = sn_delayed.cfg.cache.get(CACHE_TESTING_ITEM_NAME1)

    assert cached_value == test_value_from_cache


@pytest.mark.cache
@pytest.mark.configuration
def test_cache_as_path(cache_with_a_testing_value_saved):
    """Tests the value cached matches the pathlib.Path object retrieved from cache.as_path()."""
    sn_delayed, _ = cache_with_a_testing_value_saved

    test_value_from_cache = sn_delayed.cfg.cache.as_path(CACHE_TESTING_ITEM_NAME1)

    assert sn_delayed.cfg.location == test_value_from_cache


@pytest.mark.cache
@pytest.mark.configuration
def test_cache_saving_and_deletion_operations(cache_with_a_testing_value_saved):
    """Test basic behavior of ``snowmobile.toml`` file export."""

    # connector containing a cache object, a sample path to cache
    sn_delayed, cached_path = cache_with_a_testing_value_saved

    # two distinct names to use when caching the sample path
    cached_names = [CACHE_TESTING_ITEM_NAME1, CACHE_TESTING_ITEM_NAME2]

    # ---

    # clearing cache of these items to set starting state for tests
    for item in cached_names:
        sn_delayed.cfg.cache.clear(item)
    # - asserting only to verify state is at it should be before rest of test -
    assert not sn_delayed.cfg.cache.contains(cached_names)

    # ---

    # save two items
    sn_delayed.cfg.cache.save_all({k: cached_path for k in cached_names})

    # verify that they **are** a part of the cache
    assert sn_delayed.cfg.cache.contains(cached_names)
    # re-verify but passing them to .contains() one item at a time
    for item in cached_names:
        assert sn_delayed.cfg.cache.contains(item)

    # ---

    # clear cache of these items again; ensures the assertion on starting state
    # was a result of the .clear() removing their contents, not their never being
    # cached in the first place
    sn_delayed.cfg.cache.clear(cached_names)
    # verify they are **not** part of the cache
    assert not sn_delayed.cfg.cache.contains(cached_names)

    # ---


@pytest.mark.cache
@pytest.mark.configuration
def test_cache_dunder_methods(cache_with_a_testing_value_saved):
    """Ensuring dunder str/repr methods throw no errors"""
    assert str(cache_with_a_testing_value_saved)
    assert repr(cache_with_a_testing_value_saved)


@pytest.mark.configuration
def test_export_configuration(tmpdir):
    """Test basic behavior of ``snowmobile.toml`` file export."""
    from pathlib import Path
    from snowmobile import Configuration

    tmpdir = Path(tmpdir)
    Configuration(export_dir=tmpdir)
    assert (tmpdir / "snowmobile.toml").exists()


@pytest.mark.configuration
def test_error_on_no_configuration_file_found():
    """Test basic behavior of ``snowmobile.toml`` file export."""
    from snowmobile import Configuration

    with pytest.raises(Exception):
        _ = Configuration(config_file_nm="_an_invalid_snowmobile_test_file.txt")


@pytest.mark.configuration
def test_finds_a_valid_configuration_file():
    """"""
    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)
    cfg.cache.clear(CONFIG_FILE_NM)

    cfg2 = Configuration(config_file_nm=CONFIG_FILE_NM)
    assert cfg.location == cfg2.location


@pytest.mark.configuration
def test_configuration_json_serialization():
    """Testing serialization methods of configuration objects."""
    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)

    assert cfg.json(by_alias=True) == cfg.__json__(by_alias=True)
    assert cfg.json(by_alias=False) != cfg.json(by_alias=True)


@pytest.mark.configuration
def test_base_json_serialization():
    """Testing serialization methods of pydantic-derived objects."""
    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)

    assert cfg.script.json(by_alias=True) == cfg.script.__json__(by_alias=True)
    assert cfg.script.json(by_alias=False) != cfg.script.json(by_alias=True)


@pytest.mark.configuration
def test_get_attrs_from_obj():
    """Tests 'attrs_from_obj() method of configuration class."""

    # noinspection PyMissingOrEmptyDocstring
    class AnyClass:
        """Example class with an attribute, a method, and a property."""

        def __init__(self):
            self.any_attr = 1

        def any_callable_method(self):
            return self.any_attr + 1

        @property
        def any_property_as_well(self):
            return self.any_callable_method() + 1

    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)

    any_instance_of_any_class = AnyClass()
    attributes = cfg.attrs_from_obj(obj=any_instance_of_any_class)
    methods = cfg.methods_from_obj(obj=any_instance_of_any_class)

    assert attributes["any_attr"] == 1
    assert methods["any_callable_method"]() == 2
    assert attributes["any_property_as_well"] == 3


@pytest.mark.configuration
def test_configuration_dunder_methods():
    """Verifies appearance of __str__ and __repr__ methods."""
    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)

    assert str(cfg) == f"snowmobile.Configuration('{CONFIG_FILE_NM}')"
    assert (
        str(repr(cfg)) == f"snowmobile.Configuration(config_file_nm='{CONFIG_FILE_NM}')"
    )


@pytest.mark.configuration
def test_set_item_on_base_class():
    """Verifies behavior of __setitem__ dunder method for base class."""
    from snowmobile import Configuration

    cfg = Configuration(config_file_nm=CONFIG_FILE_NM)
    cfg.script.any_arbitrary_attribute = 1  # cfg.script derives from Base, cfg does not
    cfg.script["tw"] = 1
    assert cfg.script.any_arbitrary_attribute
    assert cfg.script.tw
