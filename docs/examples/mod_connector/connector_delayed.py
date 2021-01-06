"""
Create a delayed snowmobile.Connector object.
..docs/examples/mod_connector/connector_delayed.py
"""
import snowmobile

sn = snowmobile.Connector(delay=True)

type(sn.con)  # > None
print(sn.alive)  # > False

_ = sn.query("select 1")

type(sn.con)  # > snowflake.connector.connection.SnowflakeConnection
print(sn.alive)  # > True


# --/ stand-alone example; should run 'as is' /--
