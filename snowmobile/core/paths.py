"""
File stores default values for local file paths used by ``snowmobile``.
"""
from pathlib import Path

# ====================================
HERE = Path(__file__).absolute()
DIR_MODULES = HERE.parent
DIR_PKG_DATA = DIR_MODULES / "pkg_data"

EXTENSIONS_DEFAULT_PATH = DIR_PKG_DATA / "snowmobile_backend.toml"
DDL_DEFAULT_PATH = DIR_PKG_DATA / "DDL.sql"
# ====================================
