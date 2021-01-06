# {class}`snowmobile.Connector`

````{tabbed} Context
The attributes of {class}`snowmobile.Connector` ({class}`sn`) include the [snowmobile.Configuration](./snowmobile_toml.md#snowmobiletoml) object
as well as the {xref}`SnowflakeConnection` object, making it ubiquitous throughout {xref}`snowmobile`'s object model.

Its primary purpose is to provide an entry point that will:
1.  Locate, parse, and instantiate [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) ({class}`sn.cfg`)
2.  Establish connections to {xref}`snowflake`
3.  Execute commands/queries against the database either through its own methods or through those enabled by {xref}`SnowflakeConnection` ({class}`sn.con`)

Most often an instance of {class}`snowmobile.Connector` represents a distinct [session](https://docs.snowflake.com/en/sql-reference/sql/alter-session.html)
along with the contents of [snowmobile.toml](./snowmobile_toml.md#snowmobiletoml) that it was instantiated with.

{link-badge}`../autoapi/snowmobile/core/connector/index.html,cls=badge-secondary text-white,Related: snowmobile.core.connector API Reference,tooltip=Documentation parsed from module docstring`
````

```{toctree}
:maxdepth: 3
:hidden:

./connector_basics.md
./connector_aliases.md
./connector_sql.md
```
