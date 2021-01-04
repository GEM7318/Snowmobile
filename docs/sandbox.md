# Sandbox

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
```{literalinclude} /examples/setup/test_connection.py
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
```{literalinclude} /examples/setup/test_connection.py
:language: python
:lines: 5-8
:lineno-start: 1
```



#### 4.2: Composition context
```{literalinclude} /examples/setup/test_connection.py
:language: python
:lines: 16-19
:lineno-start: 12
```
The above statements give very brief context on the composition of `snowmobile.Connector`; please see
___ for in-depth information on the `Connector`'s object model and usage.



Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   snowmobile.SQL
   snowmobile.Configuration
   snowmobile.Connect
   snowmobile.Connector
   snowmobile.Loader
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

{mod}`snowmobile.core.connector`

{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-primary text-white,related: API Reference,tooltip=a tooltip`

```


{class}`snowmobile.Connector` ({class}`sn`) is used across the majority of {ref}`snowmobile`'s object model since its attributes include the 
[snowmobile.Configuration](./snowmobile_toml.md#snowmobiletoml) object ({attr}`sn.cfg`) as well as the {xref}`SnowflakeConnection` object ({attr}`sn.con`).
