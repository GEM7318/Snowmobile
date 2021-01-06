"""
Fixtures for snowmobile integration tests.
"""

import pytest

import time
from typing import Union, Tuple, Type
from pathlib import Path

from snowmobile.core.exception_handler import ExceptionHandler


@pytest.fixture()
def any_invalid_directory_path():
    """Invalid directory."""
    return Path("this/is/not/a/real/path")


@pytest.fixture()
def any_invalid_file_path(any_invalid_directory_path):
    """Invalid file."""
    return any_invalid_directory_path / "i-am-not-a-real-file.txt"
