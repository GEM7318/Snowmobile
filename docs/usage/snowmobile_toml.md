(header_target)=
# *snowmobile.toml*

The parsed and validated form of [snowmobile.toml](#snowmobiletoml) is a 
{class}`snowmobile.Configuration` object; all parsing of the file is done within 
{mod}`snowmobile.core.cfg`, in which sections are split at the root and fed into 
{xref}`pydantic's` glorious API to define the schema and impose (evolving) validation 
where needed.

Once validated, the {class}`Configuration` object serves as a namespace for the 
contents/structure of the configuration file and utility methods implemented on 
top of them, **with the rest of the API accessing it as the 
{attr}`~snowmobile.Connector.cfg` attribute of {class}`~snowmobile.Connector`**.

{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-secondary badge-pill text-white,API Docs: snowmobile.core.connector,tooltip=Documentation parsed from module docstring`

{class}`snowmobile.Configuration` doesn't need to be directly instantiated since it's accessible through the {attr}`~snowmobile.Connector.cfg`
attribute of {class}`snowmobile.Connector`.

We can create an instance of {class}`snowmobile.Connector` without connecting to {xref}`snowflake` by providing it with the convenience argument
`delay=True`, which will omit connecting to {xref}`snowflake` when the object is created.

```{literalinclude} ../snippets/instantiate_connector.py
:language: python
:lines: 6-14
:lineno-start: 1
```

The attributes that map to different sections of [snowmobile.toml](#snowmobiletoml) are:

```{literalinclude} ../snippets/instantiate_connector.py
:language: python
:lines: 16-20
:lineno-start: 10
```

*The full script for this section can be found [here](../snippets.md#instantiate_connectorpy).*

```{admonition} Tip
:class: tip
Each section of [snowmobile.toml](#snowmobiletoml) and attribute of {attr}`~snowmobile.Connector.cfg` outlined in lines 10-14 above maps squarely to a
specific class of {xref}`snowmobile`, the documentation for which contains more detailed information on its use.
```

## *Examples*

### Inspecting {attr}`sn.cfg`

### Clearing Cached Paths


% indentation for glossary
<style>
.tabbed-set.docutils {
    margin-bottom: unset;
    margin-top: 0;
}

.tabbed-content.docutils {
    padding-left: 1rem;
    margin-bottom: 0.5rem;
    border-top: unset;
}
</style>

## Glossary

(connection)=
````{rst-class} sn-glossary
```{tabbed} [connection]
:new-group:
*All configuration options for establishing connections to {xref}`snowflake`*
```
````

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

(loading.default-table-kwargs)=
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

```{admonition} TODO
:class: error
Finish
```

## File Contents

```{admonition} Tip
:class: tip

See [here](https://github.com/toml-lang/toml) if unfamiliar with *.toml* syntax
```

```{admonition} FYIs 
:class: TODO
Several sections below are commented out.. etc/etc
```

````{tabbed} snowmobile.toml
```{literalinclude} ../../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 1
```
````
