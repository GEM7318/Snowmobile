"""
This file holds functions that returns sets of values under tests for:
    * parsing.strip_sequence_of_patterns()
    * parsing.tag_from_stripped_line()
"""
from pathlib import Path

import snowmobile

SQL_DIR = Path(__file__).absolute().parent.parent / 'data' / 'sql'
script_paths = {k.name: k for k in SQL_DIR.rglob('*.sql')}


def get_script(script_name: str) -> snowmobile.Script:
    """Get a script object from its script name."""
    path_to_script = script_paths[script_name]
    return snowmobile.Script(
        path=path_to_script,
        sn=snowmobile.Connector(
            delay=True, config_file_nm='snowmobile_testing.toml'
        )
    )
