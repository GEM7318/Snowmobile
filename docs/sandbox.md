# snowmobile


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

## Resources
- Description


- Quick Start
    - Installation
    - Basic Usage

    
- `snowmobile.toml`
    - Description / validation
    - Caching
    - Minimum configuration
    - Structure
      - Connection
        - Credentials
        - Default-settings
      - Loading
        - file-format
        - if-exists-behavior
        - put, copy
        - export-options
      - External files
      - Query
      - Script
        - export-dir-name
        - patterns
        - qa
        - markdown
    
    
- `snowmobile` API
    - connector
        - arguments
            - delay
            - creds
            - config_file_nm
            - from_config
        - attributes
            - snowflake.connector
            - cfg
            - sql
        - methods
            - connect/disconnect/query/ex
    - loader
    - statement
      - extended classes
    - script
      - statements
      - markup

    
- [README](README.md)
- [Core-API Reference](Core-API%20Reference.md)
- [Authors](authors.md)
- [License](license.md)
- [Changelog](changelog.md)
- [Creds](creds.md)

## Other
- [Module-Index](modindex.md)
- [Index](genindex.md)




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
```{admonition} Note
- Any potential issues with validating `snowmobile.toml` or connecting to the warehouse
should be apparent upon the attempted execution of line **3** in the above snippet.
- Potential errors that occur in this step are either:
    - `snowflake.errors.DataBaseError` due to invalid credentials or connection specifications provided (most common)
    - Type errors due to values entered in *snowmobile.toml* that cannot be coerced by [pydantic](https://pydantic-docs.helpmanual.io/) 
into their defined types 
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

