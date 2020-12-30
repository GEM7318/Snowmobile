## 1: Installation
`pip install snowmobile`

## 2: Setup

### 2.1: Export **snowmobile.toml**
```python
import snowmobile
from pathlib import Path

snowmobile.Configuration(export_dir=Path.cwd())
```
Provide a target directory to the **export_dir** argument of `snowmobile.Configuration`
to export a default *snowmobile.toml* file; the above snippet exports to the current
working directory.

### 2.2: Store Credentials
The first few lines of *snowmobile.toml* are represented in the snippet below.
```{code-block} toml
:lineno-start: 2
:emphasize-lines: 4, 13

[connection]
    default-creds = ''  # will use first set of credentials below if blank

    [connection.credentials.credentials1]  # `credentials1` is a filler alias
        user = ''
        password = ''
        role = ''
        account = ''
        warehouse = ''
        database = ''
        schema = ''

    [connection.default-arguments]  # staple kwargs for snowmobile.connector.connect()
        autocommit = true
        authenticator = 'snowflake'
        timezone = 'America/Chicago'
```
All that's required for minimum configuration is:
1. **Specify a valid set of credentials within the `[connection.credentials.credentials1]` block**
2. **Modify or remove any unwanted arguments within the `[connection.default-arguments]` block**

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

### 2.4: A quick introduction, `snowmobile.Connector`
This **snowmobile.Connector** object, hereafter `sn` by convention, includes the standard Snowflake `Connector` and `Cursor` 
objects in addition **snowmobile**'s own object model. 

The below snippet outlines the attributes of `sn` touched on so far:
```{literalinclude} /examples/setup/test_connection.py
:language: python
:lineno-start: 5
:lines: 10-16
``` 

The `sn` object re-implements several forms query execution to minimize verbosity as well 
as making the two most common methods of querying data available off the same object, demonstrated
below:
```{literalinclude} /examples/setup/test_connection.py
:language: python
:lineno-start: 13
:lines: 18-22
``` 

These **snowmobile** methods and attributes can be utilized alongside or in-place of methods shipped with
**SnowflakeConnection**; for example, the below snippet uses the 




