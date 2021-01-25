"""
Create a delayed snowmobile.Snowmobile object.
..docs/snippets/connector_delayed.py
"""
import snowmobile

sn = snowmobile.Snowmobile(delay=True)

type(sn.con)     #> None
print(sn.alive)  #> False

_ = sn.query("select 1")

type(sn.con)     #> snowflake.connector.connection.SnowflakeConnection
print(sn.alive)  #> True

# -- complete example; should run 'as is' --
