"""
Export template `snowmobile.toml` to a specified directory.
../docs/snippets/export_config.py
"""
import snowmobile
from pathlib import Path

snowmobile.Configuration(export_dir=Path.cwd())

# -- complete example; should run 'as is' --
