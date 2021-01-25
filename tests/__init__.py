"""
This file is to store objects accessed by the entire test suite within the scope
of:
    *   Constant variables
    *   A base test class and an associated `idfn` for pytest IDs
    *   Static utility functions

"""
from pathlib import Path

from pydantic import BaseModel


# -- CONSTANT VARIABLES ---

CREDS = "snowmobile_testing"
CONFIG_FILE_NM = "snowmobile_testing.toml"

TESTS_ROOT = Path(__file__).absolute().parent
FILES = {p.name: p for p in TESTS_ROOT.rglob("*") if p.is_file()}


# -- BASE TEST CLASS ------


class BaseTest(BaseModel):
    """Base object for snowmobile test classes.

    Note:
        *   This class is intended to be used as a **namespace only** and
            should not be extended with additional methods unless necessary
            in order to maintain test readability.
        *   Its extensions should define a __repr__ function that will be
            retrieved by pytest when :func:`tests.idfn()` is called on its instances.
        *   Built from pydantic's BaseModel as opposed to a straight dataclass
            since it will enforce type safety, enables annotating attributes
            with clear descriptions while referencing them in code with
            succinct variable names, and is already a project dependency.

    """

    @property
    def pytest_id(self) -> str:
        """Pytest ID for console feedback during tests runs."""
        return self.__repr__()

    def __repr__(self) -> str:
        """Valid __repr__ string to fully reproduce the object under test."""
        pass

    class Config:
        """Enabling so that arbitrary types can be set on derived instances."""

        arbitrary_types_allowed = True


def idfn(val: BaseTest):
    """Retrieves :attr:`pytest_id` from derived instances of `BaseTest`."""
    assert hasattr(val, "pytest_id"), f"No 'pytest_id' for class {type(val)}"
    return val.pytest_id


# -- UTILITY FUNCTIONS ---


def get_validation_file(path1: Path, sub_dir: str = "expected_outcomes") -> Path:
    """Returns a path for the validation file given a test file path."""
    export_dir = path1.parent.parent  # expected: '.snowmobile.
    offset = path1.relative_to(export_dir)
    return export_dir / sub_dir / offset


def contents_are_identical(path1: Path, path2: Path) -> bool:
    """Reads in two paths as text files and confirms their contents are identical."""
    with open(path1, "r") as r1:
        f1 = r1.read()
    with open(path2, "r") as r2:
        f2 = r2.read()
    return f1 == f2


def script(script_name: str):
    """Get a script object from its script name."""
    from snowmobile import Script, Snowmobile

    path_to_script = FILES[script_name]
    return Script(
        path=path_to_script,
        sn=Snowmobile(config_file_nm=CONFIG_FILE_NM, creds=CREDS, delay=True),
    )
