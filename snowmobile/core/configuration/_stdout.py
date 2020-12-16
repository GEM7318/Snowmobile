"""
Console output for :class: Configuration.
"""
from __future__ import annotations

from pathlib import Path

from snowmobile.core.utils import Console


# noinspection PyMethodMayBeStatic
class Configuration(Console):
    def __init__(self):
        super().__init__()

    # Export stdout -----------------------------------------------------------
    def exporting(self, file_name: str):
        print(f"Exporting {file_name}..")

    def exported(self, file_path: Path):
        path = self.offset_path(file_path=file_path)
        print(f"<1 of 1> Exported {path}")

    # Initial stdout ----------------------------------------------------------
    def _locating(self):
        print("Locating credentials...")
        return self

    def checking_cache(self):
        print("<1 of 2> Checking for cached path...")
        return self

    def reading_provided(self):
        print("<1 of 2> Checking provided path...")
        return self

    def locating(self, is_provided: bool):
        _ = self._locating()
        return self.checking_cache() if not is_provided else self.reading_provided()

    # File found stdout -------------------------------------------------------
    def cache_found(self, file_path: Path):
        path = self.offset_path(file_path=file_path)
        print(f"<2 of 2> Cached path found at {path}")
        return self

    def provided_found(self, file_path: Path):
        path = self.offset_path(file_path=file_path)
        print(f"<2 of 2> Reading provided path {path}")
        return self

    def found(self, file_path: Path, is_provided: bool):
        return (
            self.cache_found(file_path)
            if not is_provided
            else self.provided_found(file_path)
        )

    # File not found stdout ---------------------------------------------------
    def cache_not_found(self):
        print("<2 of 2> Cached path not found")
        return self

    def traversing_for(self, creds_file_nm: str):
        print(f"\nLooking for {creds_file_nm} in local file system..")
        return self

    def not_found(self, creds_file_nm: str):
        return self.cache_not_found().traversing_for(creds_file_nm=creds_file_nm)

    # File located stdout -----------------------------------------------------
    def file_located(self, file_path: Path):
        path = self.offset_path(file_path=file_path)
        print(f"<1 of 1> Located '{file_path.name}' at {path}")
        return self

    # File cannot be found stdout ---------------------------------------------
    def cannot_find(self, creds_file_nm: str):
        print(
            f"<1 of 1> Could not find config file {creds_file_nm} - "
            f"please double check the name of your configuration file or "
            f"value passed in the 'creds_file_nm' argument"
        )
        return self
