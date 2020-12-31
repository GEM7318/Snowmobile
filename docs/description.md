`snowmobile` is a thick wrapper around the [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html) that bundles the existing Snowflake `Connection` and `Cursor` into an object model focused on configuration management and streamlining interacting with the database through Python.

At its core, `snowmobile` provides a single configuration file, *snowmobile.toml*, which can be accessed by any number of Python instances on a given machine. Internally, each component of this file is its own [pydantic](https://pydantic-docs.helpmanual.io/) object, which performs type validation of all fields upon each instantiation.

These specifications include **credentials**, **connection options**, **script execution specifications**, **file formats**, **mapping to local DDL and more**, including support for aliases such that different sets of credentials, connection arguments, and data loading specifications can be accessed through the same Python API.



