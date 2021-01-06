{xref}`snowmobile` wraps the {xref}`SnowflakeConnection` class into an object model focused on configuration
management and evolving the way Python is used to interact with the {xref}`snowflakedb`, its core features being:

{fa}`check,text-success mr-1` **Use a single configuration file, [snowmobile.toml](./usage/snowmobile_toml.md#snowmobiletoml), for any number of Python instances on a machine**

{fa}`check,text-success mr-1` **Alias different sets of credentials, connection parameters and loading specifications**

{fa}`check,text-success mr-1` **Work with sql scripts as Python objects**

{fa}`check,text-success mr-1` **Document scripts with a sql-compliant markup syntax (exports to .md)**

{fa}`check,text-success mr-1` **Tag and access individual statements from within sql files**

{fa}`check,text-success mr-1` **Map in-warehouse file formats to stored DDL and export options**

{fa}`check,text-success mr-1` **Return query results in a [SnowflakeCursor](https://docs.snowflake.com/en/user-guide/python-connector-api.html)
or a [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) from the same method**

{fa}`check,text-success mr-1` **Built-in methods to run common information schema and administrative commands**
