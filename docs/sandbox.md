# Sandbox

## connector

````{tabbed} Setting Default Credentials

Currently `creds1` is used by default since it's the first set of credentials
stored and no other alias is specified; by modifying [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml)
to the below spec, we're telling  {xref}`snowmobile`to use `creds2` for
authentication regardless of where it falls relative to all the other credentials stored:

```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

The change can be verified with:
```{literalinclude} ../snippets/connector_verify_default.py
:language: python
:lines: 1-13
```

````

````{tabbed} Issues? First Verify Assumptions
Verifying *1.b*, *1.c*, and *2* in the {ref}`Section Assumptions<assumptions>` can be done with:

```{literalinclude} ../snippets/connector_alias_order.py
:language: python
:lines: 1-24
```
````

## Alternate dropdown

<br>

`````{div} .sn-dedent-v-container
````{dropdown} Click on me to see my content!
:open:
:animate: fade-in-slide-down

*sample_table* contains:

```{div} sn-dedent-v-b-container
|   COL1 |   COL2 |
|-------:|-------:|
|      1 |      0 |
|      1 |      0 |
|      1 |      0 |
```

````

`````

<br>

`````{admonition} Fixture: **sample_table**
:class: sn-fixture, sn-dedent-v-b-container, toggle, toggle-shown

```{div} hanging
*sample_table* contains:
```
```{div} sn-dedent-v-b-container
|   COL1 |   COL2 |
|-------:|-------:|
|      1 |      0 |
|      1 |      0 |
|      1 |      0 |
```

`````

<br>

```{eval-rst}
.. dropdown:: My Content
    :open:

    Is already visible
```


## Icons


{fa}`check,text-success mr-1`

{fa}`cog`

Setup {fa}`fas cog`


{fas}`cog`

{test-custom}`anything`



````{admonition} Tip
:class: tip, sn-indent-h
**The rest of the documentation assumes**:
1.  The first credentials block has been populated with a valid set of credentials
    and its alias remains `creds1`
1.  `default-creds` has been left blank
````


## Connector


````{tabbed} Content

Establishing a connection to {xref}`snowflake` can be done with:
```{literalinclude} ../snippets/intro_connector.py
:language: python
:lineno-start: 1
:lines: 1-7
```
````

````{tabbed} Info / Errors

Three things are happening behind the scenes upon execution of line **7** in
the provided snippet and any exceptions that are raised
should provide direct feedback as to what's causing them.

---

1.  {xref}`snowmobile` will traverse your file system from the ground up
    searching for a file called [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml).
    Once found, it will cache this location for future reference and not repeat
    this step unless the file is moved.
    -   *on-failure expects* `FileNotFoundError`
2.  It will then instantiate the contents of the configuration file as
    {xref}`pydantic` objects. This ensures instant exceptions will be thrown
    if any required fields are omitted or unable to be coerced into their intended type.
    -   *on-failure expects* `ValidationError`
3.  Once validated, it will then pass the parsed arguments to the
    {meth}`snowflake.connector.connect()` method and instantiate the
    {xref}`SnowflakeConnection` object.
    -   *on-failure expects* `DataBaseError`
````

Since *creds1* is the first set of credentials stored in
[snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) and the
{ref}`default-creds<connection.default-creds>` field hasn't been set
(re: [*Setup*](connector-setup)), line **7** is implicitly invoking:
```{literalinclude} ../snippets/intro_connector.py
:language: python
:lineno-start: 8
:lines: 8-8
```

Here's some context on how to think about the basic differences in these two
{class}`~snowmobile.core.Snowmobile` objects:
```{literalinclude} ../snippets/intro_connector.py
:language: python
:lineno-start: 10
:lines: 10-12
```
{link-badge}`./sql.html,cls=badge-primary text-white,Related: snowmobile.SQL,tooltip=Documentation parsed from module docstring`

<br>


## Setup ish

````{admonition} snippet: snowmobile.toml
:class: is-content, toggle, toggle-shown
Lines 2-26 of [](./usage/snowmobile_toml.md) are outlined below; altering
configurations below this point during initial setup is not recommended.
```{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 2
:lines: 2-26
:emphasize-lines: 4, 13, 22
```
````


```{admonition}
:class: note, sn-indent-h
**The default behavior assumes [](usage/snowmobile_toml) is a unique file name for a given machine**;
the first thing {xref}`snowmobile` will do is find your [*snowmobile.toml*](./usage/snowmobile_toml)
file and cache its location; this step isn't repeated unless the file is moved,
the cache is manually cleared, or a different distribution of {xref}`snowmobile` is installed.

<a
    class="sphinx-bs badge badge-primary text-white reference external hanging"
    href="./usage/snowmobile.html#executing-raw-sql"
    title="Binding a process to a specific snowmobile.toml file">
    <span>Related: Specifying Configuration</span>
</a>
<a
    class="sphinx-bs badge badge-primary text-white reference external hanging"
    href="./usage/snowmobile_toml#clearing-cached-paths"
    title="Clearing cached file paths">
    <span>Related: Clearing Cached Paths</span>
</a>
```


```{literalinclude} ../snowmobile.core.connection.py
:caption: snowmobile.core.connection.query()
:pyobject: Connector.query
```


## Custom class
---

````{rst-class} test-custom
```{literalinclude} ../snowmobile.core.connection.py
:caption: snowmobile.core.connection.query()
:lines: 1-20
```
````

````{rst-class} test-custom-admonition
```{admonition} Special Note Title
:class: note

Special paragraph.
```
````

+++

````{rst-class} test-custom
````
```{tabbed} [connection]
*All configuration options for establishing connections to {xref}`snowflake`*
```



+++

By providing {class}`script` (below) the same instance of {class}`sn` with which {class}`t1` (above)
was instantiated, **the {xref}`SnowflakeConnection` and [Configuration](./usage/snowmobile_toml.md) is
shared amongst:**


## hlist
---

```{hlist}
:columns:
* {class}`sn:` {class}`~snowmobile.Snowmobile`
* {class}`t1:` {class}`~snowmobile.Table`
* {class}`script:` {class}`~snowmobile.Script`
```



<html>
<head>
<style>
/*p + ol {*/
/*    margin-top: -10px;*/
/*}*/
</style>
</head>

<body>

<div class="myDiv">
    <b>Its purpose is to provide an entry point that will:</b>
    <ol style="margin-top: 8px">
            <li>
            Locate, parse, and instantiate
                <a class="reference internal" href="snowmobile_toml.html#snowmobile-toml">
                           <span class="std std-doc">
                            snowmobile.toml
                           </span>
                          </a>
            </li>
        <li>Establish connections to Snowflake</li>
        <li>
            Store the SnowflakeConnection and execute commands against the database
        </li>
    </ol>
</div>

</body>
</html>




<html>
<head>
<style>
.myDiv {
  /*border: 5px outset red;*/
  /*background-color: lightblue;*/
  /*text-align: center;*/
  /*  margin: 0;*/
    line-height: 1em;
    /*padding: 0;*/
}
</style>
</head>

<body>

<div class="myDiv">
    <b>Its purpose is to provide an entry point that will:</b>
    <ol class="gem">
        <li>Locate, parse, and instantiate snowmobile.toml</li>
        <li>Establish connections to Snowflake</li>
    </ol>
</div>

</body>
</html>

<div>
    <b>Its purpose is to provide an entry point that will:</b>
    <ol class="gem">
        <li>Locate, parse, and instantiate snowmobile.toml</li>
        <li>Establish connections to Snowflake</li>
    </ol>
</div>

<br><br><br>

<html>
<head>
<style></style><title></title>
</head>
<body>
<div>
<b>Its purpose is to provide an entry point that will:</b>
<ol class="gem">
    <li>Locate, parse, and instantiate snowmobile.toml</li>
    <li>Establish connections to Snowflake</li>
</ol>
</div>
</body>
</html>

<br><br><br>

<html>
    <body>
        <b>Its purpose is to provide an entry point that will:</b>
            <ol style="margin-top: 8px">
                    <li>
                    Locate, parse, and instantiate
                        <a class="reference internal" href="snowmobile_toml.html#snowmobile-toml">
                                   <span class="std std-doc">
                                    snowmobile.toml
                                   </span>
                                  </a>
                    </li>
                <li>Establish connections to Snowflake</li>
                <li>
                    Store the SnowflakeConnection and execute commands against the database
                </li>
            </ol>
    </body>
</html>

<br><br><br>


<DL compact>
<DT><span class="fa fa-check text-success mr-1"></span><b>Use a single configuration file for any number of Python instances on a machine <i>(snowmobile.toml)</i></b>
    <dd><i>No hard-coding credentials or paths to configuration files</i>
    <dd><i>Assign aliases to credentials, connection parameters and loading specifications</i>
<DT><span class="fa fa-check text-success mr-1"></span><b>Work with sql scripts as Python objects</b>
    <dd><i>Tag and access individual statements from within sql files</i>
    <dd><i>Queue multiple scripts across shared or distinct sessions</i>
    <dd><i>Document scripts with a sql-compliant markup syntax that exports to .md</i>
<DT><span class="fa fa-check text-success mr-1"></span><b>Flexible, reliable loading of DataFrames</b>
    <dd><i><code>if_exists</code> support for ('append', 'truncate', 'replace', 'fail')</i>
    <dd><i>Generates DDL from DataFrame if table doesn't exist</i>
<DT><span class="fa fa-check text-success mr-1"></span><b>Simplified execution of raw SQL</b>
    <dd><i>Return query results in a `SnowflakeCursor` or a `DataFrame` from the same method</i>
<DT><span class="fa fa-check text-success mr-1"></span><b>Built-in methods to run common information schema and administrative commands</b>
    <dd><i>Avoid embedding sql in docstrings</i>
</DL>

````{panels}

<DL compact>
<DT><span class="fa fa-check text-success mr-1"></span><b>Use a single configuration file, <i>snowmobile.toml</i></b>
    <dd><i>Accessible from any Python instance on a machine</i>
    <dd><i>Tracked and managed by snowmobile</i>
    <dd><i>No hard-coding credentials or file paths</i>
    <dd><i>Access different configurations by assigned alias</i>
</DL>
<a class="sphinx-bs badge badge-primary text-white reference external" href="./usage/snowmobile.html#executing-raw-sql" title="Usage Documentation on Connecting to Snowflake">
<span>Related: Executing Raw SQL</span>
</a>

---

<DT><span class="fa fa-check text-success mr-1"></span><b>Work with sql scripts as Python objects</b>
    <dd><i>Tag and access individual statements from scripts</i>
    <dd><i>Queue scripts across shared or distinct sessions</i>
    <dd><i>Add metadata to statements, generate docs in .md</i>

---

<DT><span class="fa fa-check text-success mr-1"></span><b>Flexible, reliable loading of data</b>
    <dd><i>DDL generation from DataFrame</i>
    <dd><i>DataFrame vs.table compatability checks at run time</i>
    <dd><i><code>if_exists</code> support for 'truncate', append', 'replace', 'fail'</i>

---

<DT><span class="fa fa-check text-success mr-1"></span><b>Simplified execution of raw SQL</b>
    <dd><i>Access credentials & connection parameters by alias</i>
    <dd><i>Query results in a DataFrame, SnowflakeCursor, or DictCursor from the same object</i>

<a class="sphinx-bs badge badge-primary text-white reference external" href="./usage/snowmobile.html#executing-raw-sql" title="Usage Documentation on Executing Raw SQL">
<span>See Docs: Executing Raw SQL</span>
</a>

````

```{include} ./usage/script.ipynb
:source_parser: myst-nb
```


# {class}`snowmobile.Table`

{class}`snowmobile.Table` is a data loading solution that at minimum can be provided a
[**Connector**](./usage/snowmobile.md) ({class}`sn`), a {class}`pandas.DataFrame` ({class}`df`),
and a table name.

The rest of its keyword arguments are mirrored in the
{ref}`[loading.default-table-kwargs]<loading.default-table-kwargs>`
section of [snowmobile.toml](./usage/snowmobile_toml.md) and documented in
[**the API Docs for **Table**](./_build/autoapi/snowmobile/core/table/index.html).


{link-badge}`../autoapi/snowmobile/core/table/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.Table,tooltip=Documentation parsed from module docstring`


````{admonition} Note
:class: note

**Similarly to how** [**Connector**](./usage/snowmobile.md) **handles its `creds` keyword argument,**
{class}`~snowmobile.Table` **will adhere to any arguments explicitly provided and differ
to the values configured in [snowmobile.toml](./usage/snowmobile_toml) otherwise.**

The exact configuration that a given instance of {class}`~snowmobile.Table` will
differ to is defined by the state of [**snowmobile.toml**](./usage/snowmobile_toml)
at the time the [**Connector**](./usage/snowmobile.md) ({class}`sn`) was instantiated,
not its state at the time that it ({class}`~snowmobile.Table`) was instantiated;
*also outlined in [**Connector**](./usage/snowmobile.md) description.*

**The default behavior outlined below reflects those within the
{ref}`[loading]<loading.parent>` section of the
[default **snowmobile.toml** file](./usage/snowmobile_toml.md#file-contents).**

````


````{toggle} [loading]
:description: See [loading]

```{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:lines: 27-56
:lineno-start: 27
```

````


```

## 1. Default


````{tabbed} .sql (original)
```{literalinclude} ../tests/data/sql/markup_with_results.sql
:language: sql
```
````

````{tabbed} stripped .sql (.snowmobile)
```{literalinclude} ../tests/data/sql/.snowmobile/markup_with_results/(default) markup_with_results.sql
:language: sql
```
````

````{tabbed} generated .md (.snowmobile)
```{include} ../tests/data/sql/.snowmobile/markup_with_results/(default) markup_with_results.md
```
````


## Core Features

{fa}`check,text-success mr-1` **No embedding credentials within scripts**
- *`import snowmobile` is all that's required to connect*

{fa}`check,text-success mr-1` **Access multiple sets of connection parameters, credentials, and other configuration options**
- *Accessed by user-assigned alias*

{fa}`check,text-success mr-1` **Map in-warehouse file formats to stored DDL and export options**
- *Enables flexible, controlled loading of data*

{fa}`check,text-success mr-1` **Manipulate .sql scripts as Python objects**
- *Queue scripts across sessions*
- *Tag and access individual statements as a dictionary off a [Script](./_build/autoapi/snowmobile/core/script/index.html) object*
- *Document scripts with a sql-compliant markup syntax that exports as markdown*
- *Work with partitions of scripts based on assigned tags and other metadata parsed by [snowmobile](https://pypi.org/project/snowmobile/)*

{fa}`check,text-success mr-1` **Access a single configuration file, [snowmobile.toml](./usage/snowmobile_toml.md#snowmobiletoml), across any number of Python instances on a given machine**
- *Location tracking of [snowmobile.toml](./usage/snowmobile_toml.md#snowmobiletoml) is handled by [snowmobile](https://pypi.org/project/snowmobile/)*
- *A path to a specific [snowmobile.toml](./usage/snowmobile_toml.md#snowmobiletoml) file can be specified for long-standing or containerized processes*

{fa}`check,text-success mr-1` **Use a single method to return query results in a [SnowflakeCursor](https://docs.snowflake.com/en/user-guide/python-connector-api.html)
or a [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)**

{fa}`check,text-success mr-1` **Built-in methods to run common information schema and administrative commands**


## A collapsible section with markdown

<details>

  <summary>Notes</summary>

  1. A numbered
  2. list
     * With some
     * Sub bullets

</details>


<details>
  <p>More Info</p>
<h2>Heading</h2>
<p>
    1. A numbered
    2. list
     * With some
     * Sub bullets
</p>
</details>

<details>
  <p>More Info</p>
<p>
  ## Heading
  1. A numbered
  2. list
     * With some
     * Sub bullets
</p>
</details>

## Definition List Ish

:fa:`check,text-success mr-1` **No embedding credentials within scripts**
: ``import snowmobile`` *is all that's required to connect*

```{eval-rst}

:fa:`check,text-success mr-1` **No embedding credentials within scripts**
    *`import snowmobile` is all that's required to connect*

:fa:`check,text-success mr-1` **No embedding credentials within scripts**
: ``import snowmobile`` *is all that's required to connect*

```

```{eval-rst}

what
  Definition lists associate a term with a definition.

*how*
  The term is a one-line phrase, and the definition is one or more
  paragraphs or body elements, indented relative to the term.
  Blank lines are not allowed between term and definition.

```

At its core, `snowmobile` provides a single configuration file, **snowmobile.toml**, which can be accessed by any number of Python instances
on a given machine. Internally, each component of this file is its own [pydantic](https://pydantic-docs.helpmanual.io/) object, which
performs type validation of all fields upon each instantiation.


-   Use keyword arguments to alter control-flow of database errors, post-processing errors, and post-processing failures
    (assertions called on expected results of post-processing)
-   Tag certain statements to have stored post-processing and assertions run on their results before continuing
    execution of the script

## sphinx tabs

```{eval-rst}
.. tabbed:: Tab 1

    Tab 1 content

.. tabbed:: Tab 2
    :class-content: pl-1 bg-primary

    Tab 2 content

.. tabbed:: Tab 3
    :new-group:

    .. code-block:: python

        import pip

.. tabbed:: Tab 4
    :selected:

    .. dropdown:: Nested Dropdown

        Some content
```

```{eval-rst}
.. dropdown:: Example

   .. tabbed:: Script

      .. literalinclude:: ../../snowmobile/core/cfg/script.py
         :language: python
         :lineno-start: 1

```


### 2.3: `import snowmobile` and verify connection
```{literalinclude} /snippets/test_connection.py
:language: python
:lineno-start: 1
:lines: 5-8
```

```{admonition} Notes On Initial Connection
- Several things are happening behind the scenes upon execution of line **3** above:

    1.  *snowmobile* will traverse your file system from the ground up searching for a file called
        `snowmobile.toml`. Once found, it will cache this location for future reference and not repeat
        this step unless the file is moved; *on-failure expects* `FileNotFoundError`
    2.  It will then instantiate the contents of the configuration file as  [pydantic](https://pydantic-docs.helpmanual.io/) objects.
        This ensures instant exceptions will be thrown if any required fields are omitted or unable to be coerced into their
        intended type; *on-failure expects* `ValidationError`
    3.  Once validated, it will then pass the parsed arguments to the *snowflake.connector.connect()* method and instantiate the
        `SnowflakeConnector` object as an attribute; *on-failure expects* `DataBaseError`
```


## Admonitions

```{admonition} Title
:class: note

```

```{admonition} TODO
:class: todo
This is a todo.
```

```{admonition} Danger
:class: danger
This is a danger.
```

```{admonition} Error
:class: error
This is a error.
```

```{admonition} Hint
:class: hint
This is a hint.
```

```{admonition} Important
:class: important
This is important.
```

```{admonition} Tip
:class: tip
This is a tip.
```

```{admonition} Warning
:class: warning
This is a tip.
```



## Dropdown attempt

```{eval-rst}

.. dropdown:: Click on me to see my content!

    I'm the content which can be anything:

```

## HTML Details

<html>
<style>
details > summary {
  padding: 4px;
  width: 200px;
  background-color: #eeeeee;
  border: none;
  box-shadow: 1px 1px 2px #bbbbbb;
  cursor: pointer;
}

details > p {
  background-color: #eeeeee;
  padding: 4px;
  margin: 0;
  box-shadow: 1px 1px 2px #bbbbbb;
}
</style>
<body>

<details>
  <summary>Epcot Center</summary>
  <p>Epcot is a theme park at Walt Disney World Resort featuring exciting attractions, international pavilions, award-winning fireworks and seasonal special events.</p>
</details>

</body>
</html>



## Links

- [README](README.md)
- [Core-API Reference](Core-API%20Reference.md)
- [Authors](authors.md)
- [License](license.md)
- [Changelog](changelog.md)
- [Creds](creds.md)

## Other
- [Module-Index](modindex.md)
- [Index](genindex.md)


## Free Text

### snowmobile.toml

this file is parsed into a `snowmobile.Configuration` object using [pydantic's](https://pydantic-docs.helpmanual.io/) every piece the parsing and validation of `snowmobile` objects from this file is done each component of this file is its own

- Aliasing multiple credentials and connection options for easy access through the same Python API
- Specifying global connection options, credentials-specific over-rides, or over-riding both with keyword arguments passed directly to the API



 host of objects built to enable management of of configuration management options to make streamline their usage. It's designed to store credentials, connection settings, and data loading specifications in a single **snowmobile.toml** file which can be read from any virtual
environment or project on a given machine.

Its core functionality includes:

- Providing easy access to `snowflake.connector` and `snowflake.cursor` objects
- Maintain a single Snowflake configuration file for all projects on a given machine, including:
  - Caching the location of this file across projects and re-locating if its location changes
  - Optionally provide a full path to a specific configuration file if preferable for container-based solutions
- Store, alias, and access multiple sets of credentials through the same Python API
- Specify global connection settings w/ options to over-ride at the *credentials* level or through keyword arguments passed directly to the API






`snowmobile` caches its location so that users have access to  to consistent functionality across projects and environments without , which is able to be accessed by
other projects or environments on a given machine; `snowmobile` caches its location and the first time this file is found, `snowmobile` keeps track of the location of this file

will locate the first time a `snowmobile` will cache its
location From this, `snowmobile`'s object
model is instantiated which in which credentials, connection arguments,
and other configurations are stored that all projects and environments have access to.


intended to be unique for a given operating system or container which is then cached

Its design is focused on enabling:

- The use a single configuration file for credentials and other configuration options for all projects running on a given machine
- Parsing




## 4. Basic Usage

#### 4.1 Verify connection
```{literalinclude} /snippets/test_connection.py
:language: python
:lines: 5-8
:lineno-start: 1
```



#### 4.2: Composition context
```{literalinclude} /snippets/test_connection.py
:language: python
:lines: 16-19
:lineno-start: 12
```
The above statements give very brief context on the composition of `snowmobile.Snowmobile`; please see
___ for in-depth information on the `Connector`'s object model and usage.



Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   snowmobile.SQL
   snowmobile.Configuration
   snowmobile.connect
   snowmobile.Snowmobile
   snowmobile.Table
   snowmobile.Script
   snowmobile.Statement




```{admonition} Note
:class: Note

[snowmobile.toml](#snowmobiletoml) contains configuration options for the majority of {xref}`snowmobile`'s object model and shouldn't be digested all at once. The intent
of this section is to:
   1. Outline how it integrates with {xref}```snowmobile```s API and the best ways to access it
   2. Store [Field Definitions](#snowmobile_definitions) for reference throughout the rest of the documentation
```




```{admonition} See Related: API Reference
:class: tip

{mod}`snowmobile.core.connection`

{link-badge}`../autoapi/snowmobile/core/connection/index.html,cls=badge-primary text-white,related: API Reference,tooltip=a tooltip`

```


{class}`snowmobile.Snowmobile` ({class}`sn`) is used across the majority of {ref}`snowmobile`'s object model since its attributes include the
[snowmobile.Configuration](./snowmobile_toml.md#snowmobiletoml) object ({attr}`sn.cfg`) as well as the {xref}`SnowflakeConnection` object ({attr}`sn.con`).
