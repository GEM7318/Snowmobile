# {class}`snowmobile.Connector`

{class}`snowmobile.Connector` ({class}`sn`) is the cornerstone of {xref}`snowmobile`'s 
object model since it houses [Configuration](./snowmobile_toml.md#snowmobiletoml) model
as well as the {xref}`SnowflakeConnection` object.

**Its primary purpose is to provide an entry point that will:**
1.  Locate, parse, and instantiate [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) ({class}`sn.cfg`)
2.  Establish connections to {xref}`snowflake`
3.  Execute commands/queries against the database either through its own methods 
    or through those enabled by {xref}`SnowflakeConnection` ({class}`sn.con`)

Most often an instance of {class}`snowmobile.Connector` represents a distinct 
[session](https://docs.snowflake.com/en/sql-reference/sql/alter-session.html)
along with the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) 
that it was instantiated with.

{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-primary text-white,API Reference: snowmobile.core.connector,tooltip=Documentation parsed from module docstring`


## **Intro:** {class}`~snowmobile.Connector`
---


(assumptions)=
```{admonition} Section Assumptions
:class: todo

**This section assumes the following about the contents of** [**snowmobile.toml**](./snowmobile_toml.md#snowmobiletoml):
1.  The provided sections {ref}`[connection.credentials.creds1]<connection.credentials.creds1>`
    and {ref}`[connection.credentials.creds2]<connection.credentials.creds2>` are:
    1.  Populated with valid credentials
    1.  The first and second credentials stored respectively
    1.  Aliased as *creds1* and *creds2* respectively
1.  The {ref}`default-creds<connection.default-creds>` field has been left blank
```


### 1. Connecting to {xref}`snowflake`

````{tabbed} Content

Establishing a connection to {xref}`snowflake` can be done with: 
```{literalinclude} ../examples/mod_connector/intro_connector.py
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
{ref}`default-creds<connection.default-creds>` field has been left blank
(re: {ref}`Section Assumptions<assumptions>`), line **7** is implicitly invoking:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 8
:lines: 8-8
```

Here's some context on how we should think about these two
{class}`~snowmobile.core.Connector` objects:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 10
:lines: 10-12
```
{link-badge}`./sql.md,cls=badge-primary text-white,Related: snowmobile.SQL,tooltip=Documentation parsed from module docstring`

### 2. Executing raw SQL

**{xref}`snowmobile` provides three convenience methods for executing raw SQL directly 
off the {class}`~snowmobile.core.Connector`**:

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 22
:lines: 22-23
```

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 25
:lines: 25-26
```

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 28
:lines: 28-29
```

Alternatively, {xref}`snowmobile` can be used as an accessor to the 
{xref}`snowflake.connector2`; for example, the statements below are a rugged 
implementation of the three methods called on lines **22**, **25**, and **28** above,
using the {attr}`~snowmobile.Connector.con` attribute of {class}`~snowmobile.Connector`
to implement methods from the {any}`pandas` and {xref}`snowflake.connector2` APIs:

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 32
:lines: 32-34
```

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 36
:lines: 36-36
```

```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 38
:lines: 38-40
```

Which are directly comparable to **df1**, **cur1**, and **dcur1**:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 42
:lines: 42-44
```

+++
*The full script for this section can be found* [*here*](../snippets.md#quick_intro_connectorpy).


````{admonition} SnowflakeCursor / DictCursor
:class: note

```{eval-rst}

.. tabbed:: Note

   The :attr:`snowmobile.Connector.cursor` and
   :attr:`snowmobile.Connector.dictcursor` are **properties** of
   :attr:`snowmobile.Connector` that return a new instance each time they are accessed.

   Depending on the desired behavior of a :xref:`SnowflakeCursor` or
   :xref:`DictCursor`, it could be better to store an instance for re-referencing
   as opposed to repeatedly instantiate new instances of it off :class:`~snowmobile.Connector`.

.. tabbed:: In Code

   The below demonstrates the difference between calling two methods on
   the :meth:`snowmobile.Connector.cursor` property compared to on the same
   instance of :xref:`SnowflakeCursor`.

   .. literalinclude:: ../examples/mod_connector/connector_cursor_note.py
      :language: python
      :lineno-start: 1
      :lines: 1-19

```

````


````{admonition} Tip: Naming Convention
:class: tip

Adopting the following convention of variable/attribute name to associated object is
strongly encouraged as it's widely applied throughout {ref}`snowmobile`'s source code,
including in method signatures:
- **`sn`**: {class}`snowmobile.Connector`
- **`cfg`**: {class}`snowmobile.Configuration`
- **`con`**: {xref}`snowflake.connector.SnowflakeConnection`
- **`cursor`**: {xref}`snowflake.connector.cursor.SnowflakeCursor`

---

For example, see the below attributes of {class}`~snowmobile.core.Connector`:
```{literalinclude} ../examples/mod_connector/inspect_connector.py
:language: python
:lineno-start: 1
:lines: 2-14
```
````


(header_target)=
## **Credential Aliases**
---

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

```{literalinclude} ../examples/mod_connector/snowmobile_set_default_creds.toml
:language: toml
:lineno-start: 3
:lines: 3-3
```

The change can be verified with:
```{literalinclude} ../examples/mod_connector/connector_verify_default.py
:language: python
:lineno-start: 1
:lines: 1-13
```

````

````{tabbed} Issues? First Verify Assumptions
Verifying *1.b*, *1.c*, and *2* in the {ref}`Section Assumptions<assumptions>` can be done with:

```{literalinclude} ../examples/mod_connector/connector_alias_order.py
:language: python
:lineno-start: 1
:lines: 1-24
```
````

+++

(header_target)=
## **Delaying Connection**
---

Sometimes it's helpful to create a {class}`snowmobile.Connector` object without 
establishing a connection; this is accomplished by providing it with the 
convenience argument `delay=True`, which omits connecting to {xref}`snowflake`
when the object is created.

In these instances, the {attr}`~snowmobile.Connector.con` attribute will be `None` 
until a method is called on the {class}`~snowmobile.Connector` that requires a 
connection to {xref}`snowflake` at which point a call is made to
{meth}`snowflake.connector.connect()`, the connection established, and the attribute set.
```{literalinclude} ../examples/mod_connector/connector_delayed.py
:language: python
:lineno-start: 1
:lines: 1-17
```
