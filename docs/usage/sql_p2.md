##### Using {attr}`~snowmobile.SQL.nm` and {attr}`~snowmobile.SQL.obj`

Many {class}`snowmobile.SQL` methods need to know an in-warehouse object's name and type
(i.e. *dummy_table* and *table* or *sandbox* and *schema*).

These are typically passed to methods as keyword arguments, but there are times
when setting these as attributes on the {class}`snowmobile.SQL` object itself can keep code
dry if calling multiple methods on the same in-warehouse object within another function or method.


The below is a series of small examples in which the same method is called on two instances of {class}`snowmobile.SQL`,
one in which these attributes are left as defaults, and the other that has had these values explicitly set on it; **note
that each method called on the two instances of {class}`~snowmobile.SQL` produce the same results**.

````{tabbed} Setup

The below setup code does the following:
1.  Instantiates two instances of {class}`snowmobile.Connector` with the default set of credentials
1.  Sets the `auto_run` attribute on both instances of {attr}`~snowmobile.Connector.sql` to *False*; omits executing
    the generated commands throughout example
1.  Creates a **transient** *sample_table* table from the first, noting that this can be accessed from either session
    as if it were a permanent table
1.  Explicitly sets the following on the second instances of {class}`~snowmobile.Connector`:
    1.  {attr}`~snowmobile.SQL.nm` to *sample_table*
    1.  {attr}`~snowmobile.SQL.obj` to *table*

The default {attr}`~snowmobile.SQL.obj` is *table* so this isn't necessary but included for clarity of how it should be used for other object types.

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 1
:lines: 1-17
```

````

From this, the following sets of methods produce **equivalent results**:

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 21
:lines: 21-22
```

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 24
:lines: 24-25
```

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 27
:lines: 27-28
```

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 30
:lines: 30-31
```

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 33
:lines: 33-34
```

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 36
:lines: 36-37
```

To clean up after ourselves, we can drop the sample table with:

```{literalinclude} ../examples/mod_sql/sql_working_example2.py
:language: python
:lineno-start: 41
:lines: 41-41
```

The full script for this section can be found [here](../snippets.md#sql_working_example2py).
