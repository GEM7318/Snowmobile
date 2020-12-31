`snowmobile` bundles the [Snowflake Connector for Python's](https://docs.snowflake.com/en/user-guide/python-connector.html) `SnowflakeConnection` 
class into an object model focused on streamlining interaction between Python and Snowflake largely through configuration-management.

1. Configurations management, with emphasis on credentials, connection arguments, and data loading specifications
2. Standardizing common querying methods and statements against the warehouse into one object
3. Interacting with raw SQL scripts as objects in Python  

At its core, `snowmobile` provides a single configuration file, **snowmobile.toml**, which can be accessed by any number of Python instances
on a given machine. Internally, each component of this file is its own [pydantic](https://pydantic-docs.helpmanual.io/) object, which 
performs type validation of all fields upon each instantiation.

These specifications include credentials, connection arguments, loading specifications, in-warehouse file formats, mapping to local DDL, 
and SQL parsing through the same Python API.



