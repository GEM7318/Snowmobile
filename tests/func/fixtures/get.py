"""
This file holds functions that returns sets of values under tests for:
    * parsing.strip_sequence_of_patterns()
    * parsing.tag_from_stripped_line()
"""
from pathlib import Path

import snowmobile

SQL_DIR = Path(__file__).absolute().parent.parent / 'data'
total_paths = {
    **{k.name: k for k in SQL_DIR.rglob('*.sql')},
    **{k.name: k for k in SQL_DIR.rglob('*.json')}
}


def path(file_nm: str) -> Path:
    """Get a full Path to a file given its name."""
    return total_paths[file_nm]


def script(script_name: str) -> snowmobile.Script:
    """Get a script object from its script name."""
    path_to_script = path(file_nm=script_name)
    return snowmobile.Script(
        path=path_to_script,
        sn=snowmobile.Connect(
            delay=True,
            config_file_nm='snowmobile_testing.toml'
        )
    )
