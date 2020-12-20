__all__ = [
	'contents_are_identical',
	'get_validation_file',
	'path',
	'script',
]
from .get import script, path
from .file_comparison import contents_are_identical, get_validation_file
