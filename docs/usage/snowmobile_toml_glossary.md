## Glossary

(connection)=
```{tabbed} [connection]
:new-group:
*All configuration options for establishing connections to {xref}`snowflake`*
```

(connection.default-creds)=
```{tabbed} default-creds
:new-group:
*The credentials (alias) to use by default if not specified in 
{arg}`snowmobile.Connector.creds`*
```

(connection.credentials)=
```{tabbed} [connection.credentials]
:new-group:
*Groups subsections of credentials, each declared with the structure of 
``[connection.credentials.credentials_alias]``*
```
```{tabbed} +
    
The value of `credentials_alias` is the literal string to pass to the 
``creds`` argument of {class}`snowmobile.Connector` to establish the 
{xref}`snowflake` connection with those credentials.

Additional keyword-arguments can be specified in an aliased section so long 
as they are provided **verbatim** as they should be passed to the 
{meth}`snowflake.connector.connect()` method; this can be used to to map 
a specific timezone or transaction mode (for example) to a specific set of 
credentials.
```

(connection.credentials.creds1)=    
```{tabbed} [connection.credentials.creds1]
:new-group:
*Store your first set of credentials here*
```

(connection.credentials.creds2)=    
```{tabbed} [connection.credentials.creds2]
:new-group:
*Store as many more credentials as you want following this format*
```

(connection.default-arguments)=
```{tabbed} [connection.default-arguments]
:new-group:
*Staple keyword arguments to pass to {meth}`snowflake.connector.connect()`*
```
```{tabbed} +
Any arguments in this section that overlap with those stored in an aliased 
credentials block will be superceded by those associated with the credentials.
```

(loading.parent)=
```{tabbed} [loading]
:new-group:
*All configurations relating to loading data*
```

(loading.default-file-format)=
```{tabbed} default-file-format
:new-group:
*Default **file format** to use when loading local data into the warehouse*
```
```{tabbed} +
This is similar to the {ref}`connection.default-creds<connection.default-creds>`
except that instead of referring to a **credentials** alias, it's grouping 
together aliases/names of:
1.  An **in-warehouse** file format
2.  A set of **[loading.export-options]** (below)
3.  A statement tag associated with the DDL that **creates** this file format 
    (to be fetched by {xref}`snowmobile` if it's called on and doesn't yet 
    exist in the current schema)
```

(loading.put)=
```{tabbed} [loading.put]
:new-group:
*Default arguments to include in {xref}`snowflake` {meth}`put` statement*
```

(loading.copy-into)=
```{tabbed} [loading.copy-into]
:new-group:
*Default arguments to include in {xref}`snowflake` {meth}`copy into` statement*
```

(loading.export-options)=
```{tabbed} [loading.export-options]
:new-group:
*Groups subsections of export-options*
```

(loading.export-options.snowmobile_default_csv)=
```{tabbed} [loading.export-options."snowmobile_default_psv"]
:new-group:
*Default file-export options for **snowmobile_default_csv***
```
```{tabbed} +
This defines a set of keyword arguments associated with **snowmobile_default_psv** 
to be passed directly to the {meth}`pandas.DataFrame.to_csv` method when exporting
data to a local file before loading into a staging table via 
{xref}`snowflake`'s {meth}`put file from stage` statement.
```
