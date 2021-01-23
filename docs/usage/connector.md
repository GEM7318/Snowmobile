# snowmobile.Connector
---

An instance of {class}`~snowmobile.Connector` ({class}`sn`) represents a distinct 
[session](https://docs.snowflake.com/en/sql-reference/sql/alter-session.html)
along with the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
that it was instantiated with.

<p class="hanging;">Its purpose is to provide an entry point that will:</p>

1.  Locate, parse, and instantiate [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
    as a {class}`~snowmobile.Configuration` object ({class}`sn.cfg`)
1.  Establish connections to {xref}`snowflake`
1.  Store the {xref}`SnowflakeConnection` ({class}`sn.con`) and execute commands against the database 

+++

{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.connector,tooltip=Documentation parsed from docstrings`

---
<br>

(connector-examples)=
## Examples

(connector-setup)=
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

+++

### Connecting to {xref}`snowflake`
<hr class="sn-green-thick">

Establishing a connection can be done with: 
```{literalinclude} ../snippets/connector/connecting.py
:language: python
:lines: 4-6
```

Here's some basic information on the composition of `sn`:
```{literalinclude} ../snippets/connector/connecting.py
:language: python
:lines: 8-10
```

```{div} sn-indent-h-cell
<hr class="sn-blue" style="margin-top: 0.9rem; margin-bottom: -0.2rem;">
```

Given [{fa}`cog`](#examples), `sn` is implicitly using the same connection arguments
as:  
```{literalinclude} ../snippets/connector/connecting.py
:language: python
:lines: 12-12
```

Here's some context on how to think about these two instances of
{class}`~snowmobile.core.Connector`:
```{literalinclude} ../snippets/connector/connecting.py
:language: python
:lines: 14-16
```
```{div} sn-indent-cell, sn-snippet
[{fa}`file-code-o` ../connecting.py](../snippets.md#connectingpy)
```

<hr class="sn-spacer">
<hr class="sn-spacer">

```{admonition} Fixture: **sn**
:class: toggle, toggle-shown, sn-fixture
Applicable examples below make use of an equivalent `sn` without 
explicitly re-instantiating it.
```

+++
<br>

### Executing Raw SQL
<hr class="sn-green-thick">

{xref}`snowmobile` provides three convenience methods for executing raw SQL 
directly off the {class}`~snowmobile.Connector`.

````{tabbed} sn.query()
```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 9-10
```
````
````{tabbed} +
Implements {meth}`pandas.read_sql` for querying results into a {class}`pandas.DataFrame`.
+++
```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 8-18
:emphasize-lines: 5-11
```
{link-badge}`../autoapi/snowmobile/core/connector/index.html#snowmobile.core.connector.Connector.query,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.query(),tooltip=Documentation parsed from module docstring`

<hr class="sn-blue">
````

````{tabbed} sn.ex()
:new-group:
```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 22-23
```
````
````{tabbed} +
Implements {meth}`SnowflakeConnection.cursor().execute()` for executing commands 
within a {xref}`SnowflakeCursor`.
```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 21-29
:emphasize-lines: 5-10 
```
{link-badge}`../autoapi/snowmobile/core/connector/index.html#snowmobile.core.connector.Connector.ex,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.ex() ,tooltip=Documentation parsed from module docstring`

<hr class="sn-blue">
````

````{tabbed} sn.exd()
:new-group:

```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 33-34
```
````
````{tabbed} +
Implements {meth}`SnowflakeConnection.cursor(DictCursor).execute()` for 
executing commands within {xref}`DictCursor`.
```{literalinclude} ../snippets/connector/executing.py
:language: python
:lines: 32-42
:emphasize-lines: 5-12
```
{link-badge}`../autoapi/snowmobile/core/connector/index.html#snowmobile.core.connector.Connector.exd,cls=badge-secondary badge-pill text-white sn-indent-cell,API Docs: Connector.exd(),tooltip=Documentation parsed from module docstring`

<hr class="sn-blue">
````
```{div} sn-snippet
[{fa}`file-code-o` ../executing.py](../snippets.md#executingpy)
```


````{admonition} SnowflakeCursor / DictCursor
:class: note, toggle, toggle-shown, sn-indent-cell

```{eval-rst}

.. tabbed:: Note

   The accessors :attr:`~snowmobile.Connector.cursor` and
   :attr:`~snowmobile.Connector.dictcursor` are **properties** of
   :attr:`snowmobile.Connector` that return a new instance each time they are 
   accessed. Depending on the intended use of :xref:`SnowflakeCursor` or
   :xref:`DictCursor`, it could be better to store an instance for re-referencing
   as opposed to repeatedly instantiating new instances off :class:`~snowmobile.Connector`.

.. tabbed:: +

   The below demonstrates the difference between calling two methods on
   the :attr:`snowmobile.Connector.cursor` property compared to on the same
   instance of :xref:`SnowflakeCursor`.

   .. literalinclude:: ../snippets/connector_cursor_note.py
      :language: python
      :lineno-start: 1
      :lines: 1-19
```
````

---

````{admonition} Tip: Naming Convention
:class: toggle, tip, indented
The following convention of variable/attribute name to associated object is
used throughout {ref}`snowmobile`'s documentation and source code, including in 
method signatures:
- **`sn`**: {class}`snowmobile.Connector`
- **`cfg`**: {class}`snowmobile.Configuration`
- **`con`**: {xref}`snowflake.connector.SnowflakeConnection`
- **`cursor`**: {xref}`snowflake.connector.cursor.SnowflakeCursor`

---

For example, see the below attributes of {class}`~snowmobile.core.Connector`:
```{literalinclude} ../snippets/inspect_connector.py
:language: python
:lineno-start: 1
:lines: 2-14
```
````

+++

(header_target)=
### Aliasing Credentials
<hr class="sn-green-thick">

The below line in [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
denotes the set of credentials to authenticate with if one isn't
specified in the optional `creds` argument of {class}`snowmobile.Connector`.

```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

````{tabbed} Setting Default Credentials

Currently `creds1` is used by default since it's the first set of credentials 
stored and no other alias is specified; by modifying [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
to the below spec, we're telling  {xref}`snowmobile`to use `creds2` for 
authentication regardless of where it falls relative to all the other credentials stored:

```{literalinclude} ../snippets/snowmobile_set_default_creds.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

The change can be verified with:
```{literalinclude} ../snippets/connector_verify_default.py
:language: python
:lineno-start: 1
:lines: 1-13
```

````

````{tabbed} Issues? First Verify Assumptions
Verifying *1.b*, *1.c*, and *2* in the {ref}`Section Assumptions<assumptions>` can be done with:

```{literalinclude} ../snippets/connector_alias_order.py
:language: python
:lineno-start: 1
:lines: 1-24
```
````
<br>

+++

(header_target)=
### Parameter Resolution
<hr class="sn-green-thick">

```{admonition} TODO 
:class: error
Missing
```

+++

(header_target)=
### Delaying Connection
<hr class="sn-green-thick">

Sometimes it's helpful to create a {class}`~snowmobile.Connector` without 
establishing a connection; this is accomplished by providing it with the 
convenience argument `delay=True`, which omits connecting to {xref}`snowflake`
when the object is created.

In these instances, the {attr}`~snowmobile.Connector.con` attribute will be `None` 
until a method is called on the {class}`~snowmobile.Connector` that requires a 
connection to {xref}`snowflake` at which point a call is made to
{meth}`snowflake.connector.connect()`, the connection established, and the attribute set.
```{literalinclude} ../snippets/connector_delayed.py
:language: python
:lineno-start: 1
:lines: 1-17
```
<br>

+++

(header_target)=
### Specifying [snowmobile.toml](./snowmobile_toml.md)
<hr class="sn-green-thick">

```{admonition} TODO
:class: error
Missing
```
<br>

(header_target)=
### Using *ensure_alive*
<hr class="sn-green-thick">

Controlling the behavior of {class}`~snowmobile.Connector` when a connection is 
lost or intentionally killed is done through the {attr}`~snowmobile.Connector.ensure_alive` 
parameter. 

Its default value is *True,* meaning that if the  {attr}`~snowmobile.Connector.alive` 
property evaluates to *False*, **and a method is invoked that requires a 
connection,** it will re-connect to {xref}`snowflake` before continuing execution.

```{admonition} Warning
:class: warning
A re-established connection will not be on the same session as the original connection.
```

This behavior is outlined in the below snippet:
```{literalinclude} ../snippets/connector_ensure_alive.py
:language: python
:lineno-start: 1
:lines: 1-39
```

