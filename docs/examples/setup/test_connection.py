"""
Establish an initial connection and explore :class:`Connector` attributes.
../docs/examples/setup/test_connection.py
"""
import snowmobile

sn = snowmobile.Connect()  # optionally provide `creds='credentials_alias'`
assert sn.alive

df = sn.query('select 1')  # implementing pd.read_sql()
type(df)                   #> pandas.core.frame.DataFrame

cur = sn.ex('select 1')    # implementing sf.cursor.execute()
type(cur)                  #> snowflake.connector.cursor.SnowflakeCursor

type(sn)         #> snowmobile.core.connector.Connector
type(sn.cfg)     #> snowmobile.core.configuration.Configuration
type(sn.conn)    #> snowflake.connector.connection.SnowflakeConnection
type(sn.cursor)  #> snowflake.connector.cursor.SnowflakeCursor

sn.disconnect()
print(sn.alive)  #> False

# -- standalone example; should run 'as is' --
