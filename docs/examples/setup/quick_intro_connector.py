"""
Establish an initial connection and explore :class:`Connector` attributes.
../docs/examples/setup/test_connection.py
"""
import snowmobile

sn = snowmobile.Connect()  # equivalent to snowmobile.Connect(creds='creds1')

type(sn)         #> snowmobile.core.connector.Connector

type(sn.cfg)     #> snowmobile.core.configuration.Configuration
str(sn.cfg)      #> snowmobile.Configuration('snowmobile.toml')

type(sn.con)     #> snowflake.connector.connection.SnowflakeConnection
type(sn.cursor)  #> snowflake.connector.cursor.SnowflakeCursor

df1 = sn.query('select 1')                 #  == pd.read_sql()
type(df1)                                  #> pandas.core.frame.DataFrame

cur1 = sn.query('select 1', as_df=False)   #  == SnowflakeConnection.cursor().execute()
type(cur1)                                 #> snowflake.connector.cursor.SnowflakeCursor

import pandas as pd

df2 = pd.read_sql(sql='select 1', con=sn.con)
cur2 = sn.con.cursor().execute('select 1')

print(df2.equals(df1))                     #> True
print(cur1.fetchone() == cur2.fetchone())  #> True

# -- standalone example; should run 'as is' --