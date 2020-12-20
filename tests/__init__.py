"""
This file stores utility functions and constant variables accessed by all
``snowmobile`` tests.
"""
from pathlib import Path

from pydantic import BaseModel

# ===========================================
CREDS = 'snowmobile_testing'                  # credentials to use for tests
CONFIG_FILE_NM = 'snowmobile_testing.toml'    # configuration file to use for tests

TESTS_ROOT = Path(__file__).absolute().parent
FILES = {p.name: p for p in TESTS_ROOT.rglob('*') if p.is_file()}
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


# --/ ONLY TEST HELPER FUNCTIONS BELOW /---------------------------------------


def get_validation_file(path1: Path, sub_dir: str = 'expected_outcomes') -> Path:
    """Returns a path for the validation file given a test file path."""
    export_dir = path1.parent.parent  # expected: '.snowmobile.
    offset = path1.relative_to(export_dir)
    return export_dir / sub_dir / offset


def contents_are_identical(path1: Path, path2: Path) -> bool:
    """Reads in two paths as text files and confirms their contents are identical."""
    with open(path1, 'r') as r1:
        f1 = r1.read()
    with open(path2, 'r') as r2:
        f2 = r2.read()
    return f1 == f2


def script(script_name: str):
    """Get a script object from its script name."""
    from snowmobile import Script, Connect
    path_to_script = FILES[script_name]
    return Script(
        path=path_to_script,
        sn=Connect(config_file_nm=CONFIG_FILE_NM, creds=CREDS, delay=True)
    )
