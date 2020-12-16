# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import subprocess
import sys

from pathlib import Path

HERE = Path(__file__)
ROOT = HERE.parent
PACKAGE_DIR = ROOT / 'snowmobile'
sys.path.insert(0, PACKAGE_DIR)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(
#     0,
#     os.path.join(
#         os.path.abspath('source').split('docs')[0],
#         'snowmobile'
#     )
# )
# os.path.abspath('.')

# MyST Configuration ----------------------------------------------------------

# Auto-generating header anchors
# https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html#syntax-header-anchors
myst_heading_anchors = 3


source_suffix = ['.rst', '.md']

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    # 'sphinx-pydantic',
    'sphinx.ext.napoleon',
    # 'sphinx.ext.autodoc.typehints',
    # 'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
    'myst_parser',
    # 'recommonmark',
    'autoapi.extension',
    'sphinx.ext.autosectionlabel',
]

autodoc_typehints = 'description'
autosectionlabel_prefix_document = True

master_doc = 'index'
default_role = None
htmlhelp_basename = 'Recommonmarkdoc'

# Project information
project = 'snowmobile'
copyright = '2020, Grant E Murray'
author = 'Grant E Murray'

# The full version, including alpha/beta/rc tags
# release = str(
#     (
#         subprocess.check_output(['git', 'describe']).strip()
#     )
# ).split('-')[0].replace("'", '').replace('b', '')
release = '0.1.15'


source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}

autoapi_add_toctree_entry = True

autoapi_type = 'python'

autoapi_dirs = [
    '../snowmobile',
]

autoapi_ignore = [
    '__main__.py',
    '__init__.py',
    '**/stdout/*',
    '**_runner/*'
]

# Refers to dunder methods and regular methods
autoapi_python_class_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'python'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', '__main__.py', '__init__.py']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False

napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False

napoleon_use_param = True
napoleon_use_ivar = False
napoleon_use_rtype = False
napoleon_use_keyword = True

napoleon_custom_sections = 'Attributes'

# Scaffolding paste from here down ============================================

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Highlighting for code blocks
# https://sublime-and-sphinx-guide.readthedocs.io/en/latest/code_blocks.html
pygments_style = 'sphinx'

# -- External mapping ------------------------------------------------------------
python_version = '.'.join(map(str, sys.version_info[0:2]))

intersphinx_mapping = {
    'sphinx': ('http://www.sphinx-doc.org/en/stable', None),
    'python': ('https://docs.python.org/' + python_version, None),
    'matplotlib': ('https://matplotlib.org', None),
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'pandas': ('http://pandas.pydata.org/pandas-docs/stable', None),
    # 'pd': ('http://pandas.pydata.org/pandas-docs/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'sqlparse': ('https://sqlparse.readthedocs.io/en/latest/', None),
}

# Adding so that __init__ will be documented - source is from link below:
# https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method


def skip(app, what, name, obj, would_skip, options):
    # if name == "__init__":
    if name.startswith("_"):
        return False
    return would_skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


autodoc_default_options = {
    'members': 'var1, var2',
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
    'ignore-module-all': ['__main__.py'],
    'autoclass_content': 'both',
}

add_module_names = False
