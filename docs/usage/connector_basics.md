# Intro: {class}`~snowmobile.Connector`

(assumptions)=
```{admonition} Section Assumptions
:class: note

The below assumes the following about the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml):
1.  The provided sections {ref}`[connection.credentials.creds1]<connection.credentials.creds1>`
    and {ref}`[connection.credentials.creds2]<connection.credentials.creds2>` are:
    1.  Populated with valid credentials
    1.  The first and second credentials stored respectively
    1.  Aliased as *creds1* and *creds2* respectively
1.  The {ref}`default-creds<connection.default-creds>` field has been left blank
```

### 1. Connecting to {xref}`snowflake`

````{tabbed} Content

Once a valid set of credentials has been stored in [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml), a connection can be made with:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 1
:lines: 1-7
```

````

````{tabbed} Info / Errors

Several things are happening behind the scenes upon execution of line **7** in the provided snippet and any exceptions that are raised
should provide direct feedback as to what's causing them.

---

1.  {xref}`snowmobile` will traverse your file system from the ground up searching for a file called 
    [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml). Once found, it will cache this location 
    for future reference and not repeat this step unless the file is moved.
    -   *on-failure expects* `FileNotFoundError`
2.  It will then instantiate the contents of the configuration file as {xref}`pydantic` objects. This ensures instant
    exceptions will be thrown if any required fields are omitted or unable to be coerced into their intended type.
    -   *on-failure expects* `ValidationError`
3.  Once validated, it will then pass the parsed arguments to the {meth}`snowflake.connector.connect()` method and instantiate the
    {xref}`SnowflakeConnection` object.
    -   *on-failure expects* `DataBaseError` 
````

Given the {ref}`Section Assumptions<assumptions>` outlined above, creating another {class}`~snowmobile.core.Connector` with the
same set of credentials can be done with:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 8
:lines: 8-8
```

Here's some context on how we should think about these two {class}`~snowmobile.core.Connector` objects:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 10
:lines: 10-12
```

````{admonition} Tip: Naming Convention
:class: tip
 
The following mapping of variable or attribute name to associated object is applied throughout {ref}`snowmobile`'s documentation and source code,
including in method signatures:
- **`sn`**: {class}`snowmobile.Connector` 
- **`cfg`**: {class}`snowmobile.Configuration` 
- **`con`**: {xref}`snowflake.connector.SnowflakeConnection`
- **`cursor`**: {xref}`snowflake.connector.cursor.SnowflakeCursor`

---

These are some of attributes/properties on the {class}`~snowmobile.core.Connector` we just created:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 14
:lines: 14-20
```
````

### 2. Executing raw SQL

**Executing raw SQL directly off the {class}`~snowmobile.core.Connector` can be done in the following three ways**:

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

Alternatively, the attributes/properties of the {xref}`snowflake.connector` remain public so that no functionality is lost from it 
or supporting libraries. For example, the three statements below manually implement the execution component of the three methods 
called on lines 22, 25, and 28 above, using {xref}`snowmobile` **only** as a parameter and an accessor to methods from the 
{any}`pandas` and {xref}`snowflake.connector2` APIs: 

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

Which can be directly compared to our original **df1**, **cur1**, and **dcur1**:
```{literalinclude} ../examples/mod_connector/intro_connector.py
:language: python
:lineno-start: 42
:lines: 42-44
```

````{admonition} Final Note (sn.cursor / sn.dictcursor)
:class: note

```{eval-rst}

.. tabbed:: Context

   The :attr:`snowmobile.Connector.cursor` and :attr:`snowmobile.Connector.dictcursor` are **properties**
   of :attr:`snowmobile.Connector` and return a new instance each time they are accessed. 
   
   Depending on the desired behavior of a :xref:`SnowflakeCursor` or 
   :xref:`DictCursor`, it it's sometimes better be store and re-referenced
   as opposed to instantiating new instances off the 
   :class:`~snowmobile.Connector` object with each statement executed.
   
.. tabbed:: Illustration

   The below demonstrates the difference between executing two statements from 
   the :meth:`~snowmobile.Connector.cursor` property compared to calling them from the same 
   instance of :attr:`cursor`.
 
   .. literalinclude:: ../examples/mod_connector/intro_connector.py
      :language: python
      :lineno-start: 46
      :lines: 46-54

```

````
+++
The full script for this section can be found [here](../snippets.md#quick_intro_connectorpy).
