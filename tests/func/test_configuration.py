"""Test connector."""

from typing import Tuple

import pytest

from snowmobile import Connector

CACHE_TESTING_ITEM_NAME = 'test-path'


@pytest.fixture(scope='module')
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
    if sn_delayed.cfg.cache.get(CACHE_TESTING_ITEM_NAME):
        sn_delayed.cfg.cache.delete(item_name=CACHE_TESTING_ITEM_NAME)

    # save value to cache under the testing item name
    sn_delayed.cfg.cache.save(
        item_name=CACHE_TESTING_ITEM_NAME,
        item_value=value_to_cache
    )

    return sn_delayed, value_to_cache


@pytest.mark.configuration
def test_cache_save(cache_with_a_testing_value_saved):
    """Tests that the value cached matches the string value retrieved based on its name."""
    sn_delayed, cached_value = cache_with_a_testing_value_saved

    test_value_from_cache = sn_delayed.cfg.cache.get(CACHE_TESTING_ITEM_NAME)

    assert cached_value == test_value_from_cache


@pytest.mark.configuration
def test_cache_as_path(cache_with_a_testing_value_saved):
    """Tests the value cached matches the pathlib.Path object retrieved from cache.as_path()."""
    sn_delayed, _ = cache_with_a_testing_value_saved

    test_value_from_cache = sn_delayed.cfg.cache.as_path(CACHE_TESTING_ITEM_NAME)

    assert sn_delayed.cfg.location == test_value_from_cache
