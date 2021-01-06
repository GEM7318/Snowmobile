(header_target)=
# Credential Aliases

The below line in [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) denotes the set of credentials to authenticate with if one isn't
specified in the optional `creds` argument of {class}`snowmobile.Connector`.

```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

````{tabbed} Setting Default Credentials
 
Currently `creds1` is used by default since it's the first set of credentials stored and no other alias is specified;
by modifying [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) to the below spec, we're telling  {xref}`snowmobile` 
to use `creds2` for authentication regardless of where it falls relative to all the other credentials stored:

```{literalinclude} ../examples/mod_connector/snowmobile_set_default_creds.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

The change can be verified with:
```python
import snowmobile

sn = snowmobile.Connector()

assert sn.cfg.connection.default_alias == 'creds2', (
    "Something's not right here; expected default_alias =='creds2'"
)
```

````

````{tabbed} Issues: First Verify Assumptions
Verifying *1.b*, *1.c*, and *2* in the {ref}`Section Assumptions<assumptions>` can be done with:

```{literalinclude} ../examples/mod_connector/connector_alias_order.py
:language: python
:lineno-start: 1
:lines: 1-23
```
````

+++

(header_target)=
# Delaying Connection

Sometimes it can be helpful to create a {class}`snowmobile.Connector` object without establishing a connection. This is
accomplished by providing it with the convenience argument `delay=True`, which omits connecting to {xref}`snowflake` 
when the object is created.

In these instances, the {attr}`~snowmobile.Connector.con` attribute will be null until a method is called on the 
{class}`~snowmobile.Connector` that requires a connection to {xref}`snowflake` at which point a call is made to
{meth}`snowflake.connector.connect()`, the connection established, and the attribute set.

```{literalinclude} ../examples/mod_connector/connector_delayed.py
:language: python
:lines: 1-18
:lineno-start: 1
```
