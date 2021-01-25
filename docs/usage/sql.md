# SQL

{class}`~snowmobile.SQL` generates and executes raw SQL from inputs; 
it comes free as the {attr}`~snowmobile.Snowmobile.sql` attribute of 
{class}`~snowmobile.Snowmobile`, and its purpose is to provide a simple, 
accessible Python API to query metadata and execute administrative commands 
against {xref}`snowflake`.

{link-badge}`../autoapi/snowmobile/core/sql/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.sql,tooltip=Documentation parsed from module docstring`

---

```{admonition} Warning
:class: warning

Some of these methods will not ask twice before querying, altering or dropping a 
{xref}`snowflake` object if told to do so; isolated testing to ensure the API
is understood before use is recommended.
```

## Using {attr}`~snowmobile.SQL.auto_run`
<hr class="sn-green-thick">

If the keyword argument {any}`run: bool` is omitted to a method of
{class}`~snowmobile.SQL`, the current value of its {attr}`~snowmobile.SQL.auto_run`
attribute will determine whether to:
1. Return the generated SQL as a string, or
2. Execute it and return its results
     
```{note}

**{attr}`~snowmobile.SQL.auto_run` defaults to `True`, meaning by default it will 
execute the generated SQL as opposed to returning it as a string.**
```

The behavior demonstrated below encompasses all methods of {class}`snowmobile.SQL`, 
not just {meth}`snowmobile.SQL.table_sample`.

````{tabbed} Setup

Let's instantiate a {class}`~snowmobile.Snowmobile` object and create a *dummy_table* 
to use for the rest of the example.

Lines 11-12 in the below make use of {class}`snowmobile.Script` to parse a sql 
file containing a single statement and and execute it to keep from cluttering the 
snippet with the full query; the contents of the table created are the only thing 
that matters, but the script is included in the `dummy_table.sql` tab for clarity.

```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 1
:lines: 1-12
```
This creates a temp table for us called `dummy_table` with the following structure:

**dummy_table**
| SAMPLE\_KEY | SAMPLE\_METRIC1 | SAMPLE\_METRIC2 |
| :--- | :--- | :--- |
| 1 | 1 | 75 |
| 2 | 1 | 11 |
| 3 | 1 | 1 |
| 4 | 2 | 1 |
| 5 | 3 | 55 |
````

````{tabbed} dummy_table.sql

```{literalinclude} ../snippets/dummy_table.sql
:language: sql
:lineno-start: 1
:lines: 1-13
```

````

##### 1: When {attr}`~snowmobile.SQL.auto_run`=*True*
<hr class="sn-green-thick">

**By default**, calling {meth}`~snowmobile.SQL.table_sample` on our 
*dummy_table* will select an {any}`n: int` record sample from a 
table and return the results in a {class}`~pandas.DataFrame`:
```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 16
:lines: 16-19
```

Whether set to *True* or *False*, the behavior imposed by the {attr}`snowmobile.SQL.auto_run` 
can be superseded by the `run` keyword argument provided to any method:
```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 21
:lines: 21-24
```
    >>>
    select
        *
    from SANDBOX.SAMPLE_TABLE
    limit 5


### Table metadata


### Extras

##### 1: When {attr}`~snowmobile.SQL.auto_run`=*False*
<hr class="sn-green-thick">

To reverse this behavior, {attr}`~snowmobile.SQL.auto_run` can be set to *False* with:
```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 28
:lines: 28-28
```

With {attr}`~snowmobile.SQL.auto_run` disabled, the *run=False* argument can be 
omitted to produce the same string of sql created on line **21** above:
```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 30
:lines: 30-33
```

To get the {class}`~pandas.DataFrame` created on line **16**, we now need to 
explicitly pass *run=True* to the method:

```{literalinclude} ../snippets/sql_working_example.py
:language: python
:lineno-start: 35
:lines: 35-38
```

*The full script for this section can be found* [*here*](../snippets.md#sql_working_examplepy).


## Using {attr}`~snowmobile.SQL.nm` **and** {attr}`~snowmobile.SQL.obj`
---

Most {class}`snowmobile.SQL` methods need to know an in-warehouse object's name 
and type (i.e. *dummy_table* and *table* or *sandbox* and *schema*).

These can always be provided as method parameters, but there are times when
setting these values as attributes on the {class}`snowmobile.SQL` object itself can 
minimize a lot of clutter if calling multiple methods on the same in-warehouse  
object within another function or method.


The below is a series of small examples in which the same method is called on two 
instances of {class}`snowmobile.SQL`, one in which these attributes are left as 
defaults, and the other that has had these values explicitly set on it; **note
that each method called on the two instances of {class}`~snowmobile.SQL` 
produce the same results**.

````{tabbed} Setup

The below setup code does the following:
1.  Instantiates two instances of {class}`snowmobile.Snowmobile` with the default 
    set of credentials
1.  Sets the `auto_run` attribute on both instances of 
    {attr}`~snowmobile.Snowmobile.sql` to *False* to omit executing the generated 
    commands throughout example
1.  Creates a **transient** *sample_table* table so that we can 
    access it from either session as if it were a permanent table
1.  Explicitly sets the following on the **second** instances of 
    {class}`~snowmobile.Snowmobile`:
    1.  {attr}`~snowmobile.SQL.nm` to *sample_table*
    1.  {attr}`~snowmobile.SQL.obj` to *table* 

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 1
:lines: 1-17
```

````

From this, the following sets of methods produce **equivalent results**:

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 21
:lines: 21-22
```

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 24
:lines: 24-25
```

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 27
:lines: 27-28
```

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 30
:lines: 30-31
```

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 33
:lines: 33-34
```

```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 36
:lines: 36-37
```

````{admonition} Tip
:class: tip

{any}`sn2.sql.auto_run`is disabled but since {any}`sn2.sql` knows:
1. Its {attr}`~snowmobile.SQL.obj` is a *table*
1. Its {attr}`~snowmobile.SQL.obj` is in the same schema as {any}`sn2` 
1. Its {attr}`~snowmobile.SQL.nm` is *sample_table*

We can still drop it with:
```{literalinclude} ../snippets/sql_working_example2.py
:language: python
:lineno-start: 41
:lines: 41-41
```
````

*The full script for this section can be found* [*here*](../snippets.md#sql_working_example2py).
