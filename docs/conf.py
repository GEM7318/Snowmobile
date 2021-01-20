
# =============================================================================
# ========= Configuration file for the Sphinx documentation builder ===========
# =============================================================================


# -- Import Management --------------------------------------------------------
import sys

from pathlib import Path

sys.path.append(".")

HERE = Path(__file__).absolute()
ROOT = HERE.parent.parent
DOCS_DIR = ROOT / "docs"
LINKS_DIR = DOCS_DIR / "links"
EXT_DIR = DOCS_DIR / "ext"
PACKAGE_DIR = ROOT / "snowmobile"

to_insert = {
    "DOCS_DIR": DOCS_DIR,
    "LINKS_DIR": LINKS_DIR,
    "EXT_DIR": EXT_DIR,
    "PACKAGE_DIR": PACKAGE_DIR,
}
for dir_name, dir_path in to_insert.items():
    sys.path.insert(0, str(dir_path))
    print(f"<added-to-path> {dir_name}")


# -- Xref Extension -----------------------------------------------------------
# -- See docstring in ext/xref.py for more info

# noinspection PyUnresolvedReferences
from links.link import *

# noinspection PyUnresolvedReferences
from links import *


# -- Standard Options ---------------------------------------------------------

source_suffix = {
    '.md': 'myst-nb',
    '.rst': 'restructuredtext',
    '.ipynb': 'myst-nb',
    '.myst': 'myst-nb',
}

extensions = [
    "myst_nb",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "autoapi.extension",
    "xref",
    "sphinx_panels",
    "autoapi.extension",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    # "myst_parser",
    # "nbsphinx",
]

master_doc = "index"
default_role = None
language = "python"
templates_path = ["_templates"]
exclude_patterns = ["_build", "__main__.py", "__init__.py", "**.ipynb_checkpoints"]


# Project Information ---------------------------------------------------------

# from snowmobile import __version__
version = "0.0.15"

project = "snowmobile"
copyright = "2020, Grant E Murray"
author = "Grant E Murray"
# version = __version__
# release = __version__
release = version


# Sphinx Panels ---------------------------------------------------------------

# https://sphinx-panels.readthedocs.io/en/latest/

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
]
panels_add_bootstrap_css = True  # required for color in icons/etc
panels_add_fontawesome_latex = True

panels_css_variables = {
    "tabs-color-label-active": "rgba(33, 150, 243, 1)",
    "tabs-color-label-inactive": "rgba(33, 150, 243, 0.55)",
    # "tabs-color-label-inactive": "rgba(178, 206, 245, 0.62)",
    "tabs-color-overline": "rgb(207, 236, 238)",
    "tabs-color-underline": "#329ef452",
    "tabs-size-label": "0.75rem",
}

# MySt ------------------------------------------------------------------------

# https://myst-parser.readthedocs.io/en/latest/

myst_heading_anchors = 5  # auto generate anchor slugs for h1-h5
autosectionlabel_max_depth = 4
autosectionlabel_prefix_document = True

from markdown_it.extensions import deflist

myst_enable_extensions = [
    # "dollarmath",
    # "amsmath",
    # "deflist",
    # "html_image",
    # "colon_fence",
    # "smartquotes",
    # "replacements",
    # "linkify",
    # "substitution",
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]
myst_url_schemes = ("http", "https", "mailto")


# MySt Nb ---------------------------------------------------------------------
# jupyter_execute_notebooks = "cache"
jupyter_execute_notebooks = "off"

kernelspec = {
    'display_name': 'Snowmobile', 'language': 'python', 'name': 'snowmobile2'
}

nb_render_priority = {
  "html": (
            "application/vnd.jupyter.widget-view+json",
            "application/javascript",
            "text/html",
            "image/svg+xml",
            "image/png",
            "image/jpeg",
            "text/markdown",
            "text/latex",
            "text/plain",
        )
}
# default; see https://myst-nb.readthedocs.io/en/latest/use/formatting_outputs.html

# -- CopyButton ---------------------------------------------------------------

# https://sphinx-copybutton.readthedocs.io/en/latest/

# Throwing out outputs, keeping jupyter inputs and code blocks.
copybutton_selector = "div:not(.output) > div.highlight pre, div.notranslate td.code div.highlight pre"
# copybutton_selector = "div.highlight pre"  # default


# -- AutoAPI ------------------------------------------------------------------

# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html

autoapi_add_toctree_entry = False
autoapi_type = "python"
autoapi_dirs = ["../snowmobile"]
autoapi_ignore = [
    "__main__.py",
    "__init__.py",
    "**/stdout/*",
    "**_runner/*",
    "**/.snowmobile/*",
]
autoapi_python_class_content = "class"  # 'both' if __init__ as well
autoapi_member_order = "bysource"  # 'bysource' or 'groupwise'
"""
    'bysource' means 'by docstring order' for attributes and 'by actual source'
    for methods and properties.
"""

# -- ToggleButton -------------------------------------------------------------

# https://sphinx-togglebutton.readthedocs.io/en/latest/

togglebutton_hint = "expand"


# Sphinx Material / HTML Theme ------------------------------------------------

# https://bashtage.github.io/sphinx-material/

import sphinx_material

html_title = "snowmobile"
html_show_sourcelink = True
html_sidebars = {"**": ["globaltoc.html", "localtoc.html", "searchbox.html"]}
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
extensions.append("sphinx_material")

html_theme_options = {
    # 'google_analytics_account': 'UA-XXXXX',
    # 'logo_icon': '&#xe869',
    "html_minify": True,
    "html_prettify": False,
    "css_minify": True,
    "globaltoc_depth": 3,
    "globaltoc_collapse": True,
    "globaltoc_includehidden": True,
    "repo_url": "https://github.com/GEM7318/Snowmobile",
    "repo_name": "gem7318/snowmobile",
    "nav_title": "",
    "color_primary": "blue",
    "color_accent": "cyan",
    "theme_color": "2196f3",
    "body_max_width": None,
    'master_doc': True,
}
# Accent colors:
# red, pink, purple, deep-purple, indigo, blue, light-blue, cyan,
# teal, green, light-green, lime, yellow, amber, orange, deep-orange


# Other HTML Options ----------------------------------------------------------

html_static_path = ["_static"]
html_use_smartypants = True
html_use_index = True
html_domain_indices = True
html_show_sphinx = False
html_show_copyright = False

pygments_style = "sphinx"
# pygments_style = "emacs"

# html_sidebars = {}
# html_additional_pages = {}
# html_domain_indices = True
# html_split_index = False
# html_last_updated_fmt = '%b %d, %Y'


# Napoleon --------------------------------------------------------------------

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

napoleon_custom_sections = "Attributes"


# -- External URLs ------------------------------------------------------------

python_version = ".".join(map(str, sys.version_info[0:2]))

intersphinx_mapping = {
    "sqlparse": ("https://sqlparse.readthedocs.io/en/latest/", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/stable", None),
    "snowflake.connector": (
        "https://docs.snowflake.com/en/user-guide/python-connector.html",
        None,
    ),
    "snowflake": (
        "https://docs.snowflake.com/en/user-guide/python-connector.html",
        None,
    ),
    "sphinx": ("http://www.sphinx-doc.org/en/stable", None),
    "python": ("https://docs.python.org/" + python_version, None),
    "matplotlib": ("https://matplotlib.org", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "sklearn": ("http://scikit-learn.org/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
}


def autoapi_skip_member(app, what, name, obj, skip, options):
    """Exclude all private attributes, methods, and dunder methods from Sphinx."""
    import re

    exclude = re.findall("\._.*", str(obj)) or "stdout" in str(obj).lower()
    return skip or exclude


def setup(app):
    """Add autoapi-skip-member."""
    app.connect("autoapi-skip-member", autoapi_skip_member)
    app.add_css_file('css/friendly.css')
    app.add_css_file('css/application_ext.css')
