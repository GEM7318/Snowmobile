# snowmobile.Connector

````{tabbed} Context
The attributes of {class}`snowmobile.Connector` ({class}`sn`) include the [snowmobile.Configuration](./snowmobile_toml.md#snowmobiletoml) object
as well as the {xref}`SnowflakeConnection` object, making it ubiquitous throughout {xref}`snowmobile`'s object model. 

Its primary purpose is to provide an entry point that will:
1.  Locate, parse, and instantiate [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) ({class}`sn.cfg`) 
2.  Establish connections to {xref}`snowflake`
3.  Execute commands/queries against the database either through its own methods or through those enabled by {xref}`SnowflakeConnection` ({class}`sn.con`)
    
Most often an instance of {class}`snowmobile.Connector` represents a distinct [session](https://docs.snowflake.com/en/sql-reference/sql/alter-session.html) 
along with the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) that it was instantiated with. 

```` 

```{admonition} Note
:class: note

The below assumes the following about the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml):
1. The **[connection.default-creds]** has been left blank
2. The alias for the first set of credentials is *creds1*
3. The alias for the second set of credentials is *creds2*
```

### 1. Establishing a connection

````{tabbed} Content

Once a valid set of credentials has been stored in [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml), a connection can be made with:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 1
:lines: 5-7
```

```{admonition} Tip on naming convention
:class: tip
 
The following mapping of variable or attribute name to associated object is applied throughout {ref}`snowmobile`'s documentation and source code,
including in method signatures:
- **`sn`**: {class}`snowmobile.Connector` 
- **`cfg`**: {class}`snowmobile.Configuration` 
- **`con`**: {xref}`snowflake.connector.SnowflakeConnection`
```

````

````{tabbed} Background / Trouble Shooting

Several things are happening behind the scenes upon execution of line **3** in the provided snippet and any exceptions that are raised
should provide direct feedback as to what's causing them.
1.  {xref}`snowmobile` will traverse your file system from the ground up searching for a file called 
    [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml). Once found, it will cache this location 
    for future reference and not repeat this step unless the file is moved; *on-failure expects* `FileNotFoundError`
2.  It will then instantiate the contents of the configuration file as {xref}`pydantic` objects. This ensures instant
    exceptions will be thrown if any required fields are omitted or unable to be coerced into their intended type; 
    *on-failure expects* `ValidationError`
3.  Once validated, it will then pass the parsed arguments to the {meth}`snowflake.connector.connect()` method and instantiate the
    {xref}`SnowflakeConnection` object; *on-failure expects* `DataBaseError` 
````

### 2. Authenticating with multiple sets of credentials

For the purposes of this section, let's assume that 
```{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 2
:lines: 2-26
:emphasize-lines: 4, 22 
```


### .Connect()
Let's start by establishing a new connection.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 1
:lines: 1-7
```

This **snowmobile.Connector** object, `sn` hereafter, includes the standard Snowflake `Connector`as part of
**snowmobile**'s object model.

The below snippet outlines the attributes of `sn` touched on so far:
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 9
:lines: 9-15
```

The `sn` object re-implements several forms query execution to minimize verbosity as well
as make the two most common forms of querying available from the same method.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 17
:lines: 17-21
```

`sn.con: SnowflakeConnection` is left as a public attribute so that its internal methods remain available
and so that it can be passed to other libraries directly off the **snowmobile.Connector** object.

As a somewhat contrived example of this, the below statements use `sn.con` to create *df2* and *cur2* objects
with methods from Pandas and Snowflake respectively, the contents of which  mirror *df1* and *cur1*
created by `sn.query()` above.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 23
:lines: 23-29
```

The full script for this section can be found [here](../snippets.md#quick_intro_connectorpy).


{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-primary text-white,(related) snowmobile.core.connector API Reference,tooltip=Documentation parsed from module docstring`
