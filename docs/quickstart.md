## 1. Installation
`pip install snowmobile`

## 2. Export **snowmobile.toml**
Provide a target directory to the **export_dir** argument of `snowmobile.Configuration`
to export a default *snowmobile.toml* file.

```python
import snowmobile
from pathlib import Path

snowmobile.Configuration(export_dir=Path.cwd())

# -- standalone example; should run 'as is' --
```

## 3. Store Credentials
The first few lines of *snowmobile.toml* are represented in the below snippet.

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

```{admonition} Minimum Configuration Requirements 
1. Specify a valid set of credentials within the `[connection.credentials.credentials1]` block
2. Modify or remove any unwanted arguments within the `[connection.default-arguments]` block
```

## 4. Basic Usage

#### 4.1 Verify connection
```{literalinclude} /examples/setup/test_connection.py
:language: python
:lines: 5-8
:lineno-start: 1
```
```{warning}
Potential errors that occur in this step are either:
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
