# snowmobile.toml

```{toctree}
:maxdepth: 3
:hidden:

./snowmobile_toml_glossary.md
./snowmobile_toml_raw.md
```

````{tabbed} Background
:selected:

The parsed and validated form of [snowmobile.toml](#snowmobiletoml) is a {class}`snowmobile.Configuration` object, with the parent-level sections
of [snowmobile.toml](#snowmobiletoml) stored as individual attributes.

The sections are parsed as dictionaries and instantiated as {xref}`pydantic` objects in the {mod}`snowmobile.core.cfg` module to ensure type safety
and population of required fields each time a {ref}`snowmobile` object is created.

Once validated, the {class}`Configuration` object serves as a namespace for the contents/structure of the configuration file and utility methods
implemented on top of them, with the rest of the API accessing it as the {attr}`~snowmobile.Connector.cfg` attribute of {class}`snowmobile.Connector`.

````

````{tabbed} Usage
:new-group:

{class}`snowmobile.Configuration` doesn't need to be directly instantiated since it's accessible through the {attr}`~snowmobile.Connector.cfg` 
attribute of {class}`snowmobile.Connector`.

We can create an instance of {class}`snowmobile.Connector` without connecting to {xref}`snowflake` by providing it with the convenience argument 
`delay=True`, which will omit connecting to {xref}`snowflake` when the object is created.

```{literalinclude} ../examples/configuration/instantiate_connector.py
:language: python
:lines: 6-14
:lineno-start: 1
```

The attributes that map to different sections of [snowmobile.toml](#snowmobiletoml) are:

```{literalinclude} ../examples/configuration/instantiate_connector.py
:language: python
:lines: 16-20
:lineno-start: 10
```
*The full script for this section can be found [here](../snippets.md#instantiate_connectorpy).*

````
Each section of [snowmobile.toml](#snowmobiletoml) and attribute of {attr}`~snowmobile.Connector.cfg` outlined in lines 10-14 above maps squarely to a
specific class of {xref}`snowmobile`, for which the documentation contains more detailed information on its use.
