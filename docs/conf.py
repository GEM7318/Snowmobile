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

# If extensions (or modules to markup with autodoc) are in another directory,
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
myst_heading_anchors = 5


source_suffix = ['.rst', '.md']

extensions = [
    # 'sphinx.ext.autodoc',
    'myst_parser',
    'autoapi.extension',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    # 'sphinx-pydantic',
    # 'sphinx.ext.autodoc.typehints',
    # 'sphinx_autodoc_typehints',
]

autodoc_typehints = 'description'
autosectionlabel_prefix_document = True
autosectionlabel_max_depth = 4

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

autoapi_add_toctree_entry = False
autoapi_type = 'python'
autoapi_dirs = ['../snowmobile']
autoapi_ignore = [
    '__main__.py',
    '__init__.py',
    '**/stdout/*',
    '**_runner/*',
    '**/.snowmobile/*',
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


# -- HTML theme settings ------------------------------------------------------
import sphinx_material

html_show_sourcelink = True
html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
# html_theme = 'sphinx_rtd_theme'

# Set link name generated in the top bar.
html_title = 'Snowmobile'

# Material theme options (see theme.conf for more information)
html_theme_options = {

    # 'google_analytics_account': 'UA-XXXXX',
    # 'logo_icon': '&#xe869',

    'html_minify': False,
    'html_prettify': True,
    'css_minify': True,

    'globaltoc_depth': 3,
    'globaltoc_collapse': False,
    'globaltoc_includehidden': False,

    'repo_url': 'https://github.com/GEM7318/Snowmobile',
    'repo_name': 'Snowmobile',
    'nav_title': 'snowmobile',

    'color_primary': 'blue',
    'color_accent': 'cyan',
    "theme_color": "#2196f3",
}


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

# Custom sidebar templates, maps markup names to template names.
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
    'sqlparse': ('https://sqlparse.readthedocs.io/en/latest/', None),
    'pandas': ('http://pandas.pydata.org/pandas-docs/stable', None),
    'snowflake.connector': ('https://docs.snowflake.com/en/user-guide/python-connector.html', None),
    'snowflake': ('https://docs.snowflake.com/en/user-guide/python-connector.html', None),
    'sphinx': ('http://www.sphinx-doc.org/en/stable', None),
    'python': ('https://docs.python.org/' + python_version, None),
    'matplotlib': ('https://matplotlib.org', None),
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
    'sklearn': ('http://scikit-learn.org/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
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


# autodoc_default_options = {
#     'members': 'var1, var2',
#     'member-order': 'bysource',
#     'special-members': '__init__',
#     'undoc-members': False,
#     'exclude-members': '__weakref__,__str__',
#     'ignore-module-all': ['__main__.py'],
#     'autoclass_content': 'class',
# }

# add_module_names = False
