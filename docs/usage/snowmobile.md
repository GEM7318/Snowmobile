(usage/snowmobile)=
# Snowmobile
---

An instance of {class}`~snowmobile.Snowmobile` ({class}`sn`) represents a distinct 
[session](https://docs.snowflake.com/en/sql-reference/sql/alter-session.html)
along with the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
that it was instantiated with.

```{div} sn-dedent-v-t-h, sn-dedent-v-b-h
Its purpose is to provide an entry point that will:
```
1.  Locate, parse, and instantiate [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
    as a {class}`~snowmobile.Configuration` object ({class}`sn.cfg`)
1.  Establish connections to {xref}`snowflake`
1.  Store the {xref}`SnowflakeConnection` ({class}`sn.con`) and execute commands against the database 

+++

{link-badge}`../autoapi/snowmobile/core/connection/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.connection,tooltip=Documentation parsed from docstrings`

---
<br>

## Contents

- [Connecting](usage/snowmobile/connecting)
- [Executing Raw SQL](usage/snowmobile/executing)
- [Aliasing Credentials](usage/snowmobile/aliasing-credentials)
- [Parameter Resolution](usage/snowmobile/parameter-resolution)
- [Delaying Connection](usage/snowmobile/delaying-connection)
- [Specifying snowmobile.toml](usage/snowmobile/specifying-snowmobiletoml)
- [Using *ensure_alive*](usage/snowmobile/using-ensure-alive)

<br>
<hr class="sn-spacer">

(target)=
```{admonition} Setup
:class: toggle, todo, is-setup, toggle-shown
**This section assumes the following about the contents of** [**snowmobile.toml**](./snowmobile_toml.md#snowmobiletoml):
1.  {ref}`[connection.credentials.creds1] <connection.credentials.creds1>`
    and {ref}`[connection.credentials.creds2]<connection.credentials.creds2>` are:
    1.  Populated with valid credentials
    1.  The first and second credentials stored respectively
    1.  Aliased as *creds1* and *creds2* respectively
1.  {ref}`default-creds<connection.default-creds>` has been left blank
```

<br>
<hr class="sn-spacer">
<hr class="sn-spacer">

(usage/snowmobile/connecting)=
### Connecting to {xref}`snowflake`
<hr class="sn-green-thick">

```{div} sn-pre-code
Establishing a connection can be done with:
``` 
```{literalinclude} ../snippets/snowmobile/connecting.py
:language: python
:lines: 4-6
```

```{div} sn-pre-code 
Here's some basic information on the composition of `sn`:
```
```{literalinclude} ../snippets/snowmobile/connecting.py
:language: python
:lines: 8-10
```

```{div} sn-indent-h-cell
<hr class="sn-green" style="margin-top: 0.9rem; margin-bottom: -0.2rem;">
```

```{div} sn-pre-code 
Given [{fa}`cog`](#target), `sn` is implicitly using the same connection arguments
as:  
```
```{literalinclude} ../snippets/snowmobile/connecting.py
:language: python
:lines: 12-12
```

```{div} sn-pre-code 
Here's some context on how to think about these two instances of
{class}`~snowmobile.core.Snowmobile`:
```
```{literalinclude} ../snippets/snowmobile/connecting.py
:language: python
:lines: 14-16
```
```{div} sn-indent-cell, sn-snippet
[{fa}`file-code-o` ../connecting.py](../snippets.md#connectingpy)
```

<br>

```{admonition} Fixture: **sn**
:class: toggle, toggle-shown, sn-fixture
Applicable examples below make use of an equivalent `sn` without 
explicitly re-instantiating it.
```
+++
<br>
<hr class="sn-spacer">

(usage/snowmobile/executing)=
### Executing Raw SQL
<hr class="sn-green-thick">

{xref}`snowmobile` provides three convenience methods for executing raw SQL 
directly off the {class}`~snowmobile.Snowmobile`.

````{tabbed} sn.query()
```{literalinclude} ../snippets/snowmobile/executing.py
:language: python
:lines: 10-11
```
````
````{tabbed} +

  Implements {meth}`pandas.read_sql` for querying results into a {class}`pandas.DataFrame`. 

  ```{literalinclude} ../snippets/snowmobile/executing.py
  :language: python
  :lines: 9-18
  :emphasize-lines: 5-10
  ```

  {link-badge}`../autoapi/snowmobile/core/connection/index.html#snowmobile.core.connection.Snowmobile.query,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.query(),tooltip=Documentation parsed from module docstring`

  ```{div} sn-indent-h-cell
  <hr class="sn-green">
  ```
  
````

````{tabbed} sn.ex()
:new-group:
```{literalinclude} ../snippets/snowmobile/executing.py
:language: python
:lines: 22-23
```
````
````{tabbed} +

  Implements {meth}`SnowflakeConnection.cursor().execute()` for executing commands 
  within a {xref}`SnowflakeCursor`.

  ```{literalinclude} ../snippets/snowmobile/executing.py
  :language: python
  :lines: 21-28
  :emphasize-lines: 5-8 
  ```

  {link-badge}`../autoapi/snowmobile/core/connection/index.html#snowmobile.core.connection.Snowmobile.ex,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.ex() ,tooltip=Documentation parsed from module docstring`

  ```{div} sn-indent-h-cell
  <hr class="sn-green">
  ```
````

````{tabbed} sn.exd()
:new-group:
```{literalinclude} ../snippets/snowmobile/executing.py
:language: python
:lines: 32-33
```
````
````{tabbed} +

  Implements {meth}`SnowflakeConnection.cursor(DictCursor).execute()` for 
  executing commands within {xref}`DictCursor`. 

  ```{literalinclude} ../snippets/snowmobile/executing.py
  :language: python
  :lines: 31-40
  :emphasize-lines: 5-10
  ```

  {link-badge}`../autoapi/snowmobile/core/connection/index.html#snowmobile.core.connection.Snowmobile.exd,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.exd(),tooltip=Documentation parsed from module docstring`

  ```{div} sn-indent-h-cell
  <hr class="sn-green">
  ```
````

```{div} sn-snippet
[{fa}`file-code-o` ../executing.py](../snippets.md#executingpy)
```

+++

````{admonition} SnowflakeCursor / DictCursor
:class: note, toggle, toggle-shown, sn-indent-cell, sn-indent-h-sub-cell-right

```{eval-rst}

.. tabbed:: Note

   The accessors `sn.cursor` and `sn.dictcursor` are **properties** of
   :attr:`~snowmobile.Snowmobile` that return a new instance each time they are 
   accessed. Depending on the intended use of :xref:`SnowflakeCursor` or
   :xref:`DictCursor`, it could be better to store an instance for re-referencing
   as opposed to repeatedly instantiating new instances off `sn`.

.. tabbed:: +

   The below demonstrates the difference between calling two methods on
   the :attr:`snowmobile.Snowmobile.cursor` property compared to on the same
   instance of :xref:`SnowflakeCursor`.

   .. literalinclude:: ../snippets/connector_cursor_note.py
      :language: python
      :lines: 1-19
```
````

`````{admonition} Naming Convention
:class: tip, toggle, toggle-shown, sn-indent-cell, sn-indent-h-sub-cell-right

````{tabbed} Tip
The following convention of variable/attribute name to associated object is
used throughout {ref}`snowmobile`'s documentation and source code, including in 
method signatures:
- **`sn`**: {class}`snowmobile.Snowmobile`
- **`cfg`**: {class}`snowmobile.Configuration`
- **`con`**: {xref}`snowflake.connector.SnowflakeConnection`
- **`cursor`**: {xref}`snowflake.connector.cursor.SnowflakeCursor`
````

````{tabbed} +
```{div} sn-pre-code
For example, see the below attributes of {class}`~snowmobile.core.Snowmobile`:
```
```{literalinclude} ../snippets/inspect_connector.py
:language: python
:lines: 2-14
```

<hr class="sn-spacer">

````
`````

<hr class="sn-spacer">
<hr class="sn-spacer">

(usage/snowmobile/aliasing-credentials)=
### Aliasing Credentials
<hr class="sn-green-thick">

The [default snowmobile.toml](./snowmobile_toml.md#file-contents) contains
scaffolding for two sets of credentials, aliased `creds1` and `creds2` respectively.

By changing `default-creds = ''` to `default-creds = 'creds2'`, 
[Snowmobile](/usage/snowmobile) will use the credentials from `creds2` 
regardless of where it falls relative to all the other credentials stored.

```{div} sn-pre-code 
The change can be verified with:
```
```{literalinclude} ../snippets/snowmobile/verify_default_alias_change.py
:language: python
:lines: 1-10
```

<br>
<hr class="sn-spacer">
<hr class="sn-spacer">

(usage/snowmobile/parameter-resolution)=
### Parameter Resolution
<hr class="sn-green-thick">

```{div} sn-dedent-v-b-h
**`sn` will look in three places (in the following order)** to compile the 
connection arguments that it passes to {xref}`snowflake.connector.connect()` 
when establishing a connection:
```
1. {ref}`[connection.default-arguments]<connection.default-arguments>`
1. {ref}`[connection.credentials.alias_name]<connection.credentials.creds1>`
1. Keyword arguments passed to {meth}`snowmobile.connect()`

```{div} sn-dedent-v-b-h
If the same argument is defined in multiple sources, <b>the <u>last</u> 
value found will take precedent;</b> the purpose of this resolution order is 
to enable:
```
-   Embedding connection arguments (e.g. timezone or transaction mode) 
    within an aliased credentials block whose **values** differ from defaults
    specified in {ref}`[connection.default-arguments]<connection.default-arguments>`
-   Superseding any connection parameters configured in [](./snowmobile_toml.md) 
    with keyword arguments passed directly to {meth}`snowmobile.connect()`
    

`````{admonition} Details
:class: toggle, is-content, sn-indent-cell, sn-dedent-v-t-h-container, sn-indent-h-sub-cell-right
 
```{div} sn-pre-code, sn-pre-code-dedent
  The {ref}`[connection.default-arguments]<connection.default-arguments>` and 
  {ref}`[connection.credentials.alias_name]<connection.credentials.creds1>` 
  are merged as the 
  {attr}`~snowmobile.core.cfg.connection.Connection.connect_kwargs` 
  property of {attr}`~snowmobile.core.cfg.connection.Connection` with: 
```
+++
```{code-block} python
:emphasize-lines: 4,4

    @property
    def connect_kwargs(self) -> Dict:
        """Arguments from snowmobile.toml for `snowflake.connector.connect()`."""
        return {**self.defaults, **self.current.credentials}
```
+++
```{div} sn-pre-code, sn-post-code, sn-pre-code-dedent
  {attr}`~snowmobile.core.cfg.connection.Connection.connect_kwargs`
  is then combined with keyword arguments passed to {meth}`snowmobile.connect()` 
  within the method itself as the {attr}`~snowmobile.Snowmobile.con` attribute
  of `sn` is being set:
```
```{code-block} python
:emphasize-lines: 8-9

    def connect(self, **kwargs) -> Snowmobile:
        """Establishes connection to Snowflake.
        ...
        """
        try:
            self.con = connect(
                **{
                    **self.cfg.connection.connect_kwargs,  # snowmobile.toml
                    **kwargs,  # any kwarg over-rides
                }
            )
            self.sql = sql.SQL(sn=self)
            print(f"..connected: {str(self)}")
            return self

        except DatabaseError as e:
            raise e
```
<hr class="sn-spacer">
`````

<br>

(usage/snowmobile/delaying-connection)=
### Delaying Connection
<hr class="sn-green-thick">

Sometimes it's helpful to create a {class}`~snowmobile.Snowmobile` without 
establishing a connection; this is accomplished by providing it with the 
convenience argument `delay=True`, which omits connecting to {xref}`snowflake`
when the object is created.

In these instances, the {attr}`~snowmobile.Snowmobile.con` attribute will be `None` 
until a method is called on the {class}`~snowmobile.Snowmobile` that requires a 
connection; at this point a call is made to {meth}`snowflake.connector.connect()`, 
the connection established, and the attribute set.
```{literalinclude} ../snippets/connector_delayed.py
:language: python
:lines: 1-17
```
+++

<br>
<hr class="sn-spacer">

(usage/snowmobile/specifying-snowmobiletoml)=
### Specifying [snowmobile.toml](./snowmobile_toml.md)
<hr class="sn-green-thick">

```{admonition} TODO
:class: error
Missing
```
<br>

(usage/snowmobile/using-ensure-alive)=
### Using *ensure_alive*
<hr class="sn-green-thick">

Controlling the behavior of {class}`~snowmobile.Snowmobile` when a connection is 
lost or intentionally killed is done through the {attr}`~snowmobile.Snowmobile.ensure_alive` 
parameter. 

Its default value is *True,* meaning that if the  {attr}`~snowmobile.Snowmobile.alive` 
property evaluates to *False*, **and a method is invoked that requires a 
connection,** it will re-connect to {xref}`snowflake` before continuing execution.

```{admonition} Warning
:class: warning, sn-dedent-v-container, sn-indent-cell, sn-indent-h-sub-cell-right
A re-established connection will not be on the same session as the original connection.
```

`````{admonition} Details
:class: toggle, is-content, sn-indent-cell, sn-dedent-v-t-h-container, sn-indent-h-sub-cell-right

The behavior described above is demonstrated in the below snippet:

```{literalinclude} ../snippets/snowmobile/ensure_alive.py
:language: python
:lines: 1-39
```
<hr class="sn-spacer">
`````
