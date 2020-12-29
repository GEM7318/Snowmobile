"""
Export template `snowmobile.toml` to a specified directory.
../docs/examples/setup/export_config.py
"""
import snowmobile
from pathlib import Path

snowmobile.Configuration(export_dir=Path.cwd())

# -- standalone example; should run 'as is' --
