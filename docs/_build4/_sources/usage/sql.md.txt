# {class}`snowmobile.SQL`

{class}`snowmobile.SQL` generates and executes raw SQL statements based on inputs; an instance of
{class}`~snowmobile.SQL` is stored as a {class}`~snowmobile.Connector` attribute, {attr}`~snowmobile.Connector.sql`, and will execute
statements on the connection associated with that {class}`~snowmobile.Connector` object.

Its purpose is to provide a succinct way to execute administrative and information-schema-based statements
from within Python without embedding SQL in docstrings and cluttering code/destroying readability.

```{admonition} Be Mindful
:class: warning

This object should be used thoughtfully; it will not ask twice before dropping a {xref}`snowflake` object, and isolated 
testing to ensure certain methods are understood before using them is **strongly** recommended. 
```

```{toctree}
:maxdepth: 3
:hidden:

./sql_p1.md
./sql_p2.md
```
