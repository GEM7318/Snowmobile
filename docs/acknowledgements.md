# Acknowledgements

The purpose of this page is to acknowledge projects that are leveraged
in the construction of the {xref}`snowmobile` API and documentation.

<br>

<h2 class="hanging">API</h2>
<hr class="sn-blue hanging">

+++
[**appdirs**](https://pypi.org/project/appdirs/)
-   The {class}`AppDirs` class is used to determine the application data
    location across operating systems in {mod}`snowmobile.core.cache`.
    
+++
**{any}`pandas`**
-   {meth}`pandas.sql.io.get_schema()` is used to generate generic DDL 
    from a raw {class}`~pandas.DataFrame` within {class}`snowmobile.Table`
-   {meth}`pandas.read_sql()` is used to read the results of a query
    directly into a {class}`~pandas.DataFrame`
    
+++ 
**{xref}`pydantic`**
-   {xref}`pydantic` is used to define, parse, and validate the configuration
    model in {any}`snowmobile.core.cfg`
    
+++ 
**{any}`sqlparse`**
-   The {meth}`sqlparse.parsestream()` method is used for the **initial** parsing
    of a raw SQL file into individual statements.

<hr class="sn-blue">

<br>

<h2 class="hanging">Documentation</h2>
<hr class="sn-blue">

+++
Code Parsing
-   [**AutoAPI**](https://autoapi.readthedocs.io/) is used to generate the
    [API reference documentation](./autoapi/snowmobile/core/index)
    from {xref}`snowmobile`'s source code.

+++
Docs Parsing
-   The rest of the docs are built on top of the glorious work being 
    done by the [**The Executable Book Project**](https://github.com/executablebooks),
    most specifically:
    -   [**MySt**](https://myst-parser.readthedocs.io/en/latest/) which bundles 
        markdown and reStructuredText into the same markup syntax
    -   [**MySt-NB**](https://myst-nb.readthedocs.io/en/latest/) which enables the use
        of [**Notebooks**](https://jupyter.org/) to generate valid documentation
    -   [**Sphinx-copybutton**](https://sphinx-copybutton.readthedocs.io/en/latest/)
    -   [**Sphinx-togglebutton**](https://github.com/executablebooks/sphinx-togglebutton)
    -   [**Sphinx-abs**](https://sphinx-tabs.readthedocs.io/en/latest/#)
    
+++
Theme
-   [**Material for Sphinx**](https://bashtage.github.io/sphinx-material/) 
    is used as the theme for this site

<hr class="sn-blue">

<br>
