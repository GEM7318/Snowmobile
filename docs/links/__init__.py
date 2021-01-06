"""
External links extensions for sphinx.
https://sublime-and-sphinx-guide.readthedocs.io/en/latest/references.html
"""

# from os.path import dirname, basename, isfile
#
# from pathlib import Path
# current_dir = Path.cwd().absolute()
#
# # modules = [f for f in current_dir.iterdir() if f.is_file()]
# modules = [basename(f)[:-3] for f in current_dir.iterdir() if f.is_file()]
# __all__ = modules
# print(__all__)

__name__ = "links"

from os.path import dirname, basename, isfile

import glob

modules = glob.glob(dirname(__file__) + "/*.py")

__all__ = [basename(f)[:-3] for f in modules if isfile(f)]
