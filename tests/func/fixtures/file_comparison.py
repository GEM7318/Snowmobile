"""
This file holds functions that returns sets of values under tests for:
    * parsing.strip_sequence_of_patterns()
    * parsing.tag_from_stripped_line()
"""
from pathlib import Path


def get_validation_file(path1: Path, sub_dir: str = 'expected_outcomes') -> Path:
    """Returns a path for the validation file given a test file path."""
    export_dir = path1.parent.parent  # expected: '.snowmobile.
    offset = path1.relative_to(export_dir)
    return export_dir / sub_dir / offset


def contents_are_identical(path1: Path, path2: Path) -> bool:
    """Reads in two paths as text files and confirms their contents are identical.

    Args:
        path1 (Path):
            1st file path.
        path2 (Path):
            2nd file path.

    Returns (bool):
        Boolean indication of the files being identical.

    """
    with open(path1, 'r') as r1:
        f1 = r1.read()
    with open(path2, 'r') as r2:
        f2 = r2.read()
    return f1 == f2
