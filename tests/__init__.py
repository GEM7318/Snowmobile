"""
This file stores utility functions and constant variables accessed by all
``snowmobile`` tests.
"""
from pathlib import Path

from pydantic import BaseModel

# == HARD CODED VALUES USED IN TEST SUITE ==
CREDS = 'snowmobile_testing'
CONFIG_FILE_NM = 'snowmobile_testing.toml'
TESTING_ROOT = Path(__file__).absolute()
# ==========================================


# noinspection PyProtectedMember
class BaseTest(BaseModel):
    """Base object for snowmobile test classes.

    Note:
        *   This class is intended to be used as a **namespace only** and
            should not be extended with additional methods unless necessary
            in order to maintain test readability.
        *   Built from pydantic's BaseModel as opposed to a vanilla data class
            as it's already a dependency of the project and allows for
            annotating attributes with clear descriptions while referencing
            them in code with more succinct variable names.
        *   Its extensions should define a __repr__ function that will be
            retrieved by pytest via the `pytest_id` property when `idfn` is
            called on its instances.

    """

    @property
    def pytest_id(self) -> str:
        """Test ID for pytest output; defaults to value of __repr__()."""
        return self.__repr__()

    def __repr__(self) -> str:
        """Full __repr__ string to reproduce the object under test."""
        pass

    class Config:
        arbitrary_types_allowed = True


# noinspection SpellCheckingInspection
def idfn(val: BaseTest):
    """Retrieves :attr:`pytest_id` from derived instances of `BaseTest`."""
    assert hasattr(val, 'pytest_id'), f"No 'pytest_id' for class {type(val)}"
    return val.pytest_id
