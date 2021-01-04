## snowmobile.toml


````{tabbed} Context

The parsed and validated form of [snowmobile.toml](#snowmobiletoml) is a {class}`snowmobile.Configuration` object, with the parent-level sections
of [snowmobile.toml](#snowmobiletoml) stored as individual attributes.

The sections are parsed as dictionaries and instantiated as {xref}`pydantic` objects in the {mod}`snowmobile.core.cfg` module to ensure type safety
and population of required fields each time a {ref}`snowmobile` object is created. 

Once validated, the {class}`Configuration` object serves as a namespace for the contents/structure of the configuration file and utility methods
implemented on top of them, with the rest of the API accessing it as the `cfg` attributet of {class}`Connector` (e.g. {class}`snowmobile.Connector.cfg`).

````

````{tabbed} Usage

{class}`snowmobile.Configuration` doesn't need to be directly instantiated since it's directly accessible through the **`cfg`** attribute of 
{class}`snowmobile.Connector`. 
  
We can create an instance of {class}`snowmobile.Connector` without connecting to {xref}`snowflake` by providing the
convenience argument `delay=True`, which will omit connecting to {xref}`snowflake` when the object is created.

```{literalinclude} ../examples/configuration/instantiate_connector.py
:language: python
:lines: 6-14
:lineno-start: 1
```
\
The attributes that map to different sections of [snowmobile.toml](#snowmobiletoml) are: 

```{literalinclude} ../examples/configuration/instantiate_connector.py
:language: python
:lines: 16-20
:lineno-start: 10
``` 
*The full script for this section can be found [here](../snippets.md#instantiate_connectorpy).*


Each section of [snowmobile.toml](#snowmobiletoml) and attribute of **`sn.cfg`** outlined in lines 10-14 above maps squarely to a
specific class of {xref}`snowmobile`, the documentation for which contains more detailed information on the purpose and use of a given section.


````


````{tabbed} Field Definitions

```{admonition} Tip
:class: tip

See [here](https://github.com/toml-lang/toml) if unfamiliar with *.toml* syntax 
```



```{eval-rst}

.. _target:: snowmobile_definitions

:``[connection]``: Groups all configuration options for establishing connections to :xref:`snowflake`

:``[connection.credentials]``: 
    Groups subsections of credentials, each declared with the structure of ``[connection.credentials.credentials_alias]``
    
    The value of `credentials_alias` is the literal string to pass to the ``creds`` argument of :class:`snowmobile.Connector` to establish 
    the :xref:`snowflake` connection with those credentials.

    Additional keyword-arguments can be specified in an aliased section so long as they are provided **verbatim** as they should be 
    passed to the :meth:`snowflake.connector.connect()` method; this can be used to to map a specific timezone or transaction mode (for example) 
    to a specific set of credentials.

:``[connection.default-arguments]``:
    Arguments to include with every connection
    
    Any arguments in this section that overlap with those stored in an aliased credentials block will be superceded by those associated with the credentials.
     
```

````
