"""
Base class for all module-level Stdout objects.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Union


class Console:
    def __init__(self):
        pass

    @staticmethod
    def offset_path(
        file_path: Union[str, Path],
        root_dir_nm: Optional[str] = None,
        indent: Optional[str] = None,
        output: bool = False,
    ) -> str:
        """Gets truncated string for file path relative to a root directory.

        Args:
            file_path (Union[str, Path]):
                Full string or Path to the file.
            root_dir_nm (str):
                Directory name to anchor truncated file path to.
            indent (str):
                Optional character to indent by (e.g. '\t')
            output (bool):
                Option to print the string as well as return it.

        Returns (str):
            Truncation of a path for console output.

        """
        indent = indent or str()
        root_dir = root_dir_nm or file_path.parent.name
        root_path = file_path.parent
        for p in file_path.parents:
            if p.name == root_dir:
                root_path = p
                break
        offset_path = file_path.relative_to(root_path)
        stdout = f"{indent}../{root_path.name}/{offset_path.as_posix()}"
        if output:
            print(stdout)
        return stdout
