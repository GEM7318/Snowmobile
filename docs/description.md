```{eval-rst}
A library focused on streamlining interaction with :xref:`snowflake` through Python for Data Scientists
and Data Engineers.

:xref:`snowmobile` wraps the :xref:`SnowflakeConnection` into an object model that is built around
configuration management and evolving the implementation of common tasks executed against the warehouse,
with its core features being:
```

At its core, `snowmobile` provides a single configuration file, **snowmobile.toml**, which can be accessed by any number of Python instances
on a given machine. Internally, each component of this file is its own [pydantic](https://pydantic-docs.helpmanual.io/) object, which
performs type validation of all fields upon each instantiation.

Add features..

{fa}`check,text-success mr-1` **no embedding of credentials within scripts;** `import snowmobile` is all that's required to establish a connection.

{fa}`check,text-success mr-1` **rotate credentials and connection arguments on the fly;** accessed by assigned alias.

{fa}`check,text-success mr-1` **map in-warehouse file formats to DDL and export options for standardized loading of data**



