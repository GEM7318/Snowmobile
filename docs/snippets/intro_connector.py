"""
.
../snippets/intro_connector.py
"""
import snowmobile

sn = snowmobile.connect()
sn2 = snowmobile.connect(creds="creds1")

sn.cfg.connection.current == sn2.cfg.connection.current  #> True
sn.sql.current("schema") == sn2.sql.current("schema")    #> True
sn.sql.current("session") == sn2.sql.current("session")  #> False

type(sn)         #> snowmobile.core.connection.Snowmobile

type(sn.cfg)     #> snowmobile.core.configuration.Configuration
str(sn.cfg)      #> snowmobile.Configuration('snowmobile.toml')

type(sn.con)     #> snowflake.connector.connection.SnowflakeConnection
type(sn.cursor)  #> snowflake.connector.cursor.SnowflakeCursor

df1 = sn.query("select 1")  #  == pd.read_sql()
type(df1)                   #> pandas.core.frame.DataFrame

cur1 = sn.ex("select 1")    #  == SnowflakeConnection.cursor().execute()
type(cur1)                  #> snowflake.connector.cursor.SnowflakeCursor

dcur1 = sn.exd("select 1")  #  == SnowflakeConnection.cursor(DictCursor).execute()
type(dcur1)                 #> snowflake.connector.DictCursor


import pandas as pd

df2 = pd.read_sql(sql="select 1", con=sn.con)

cur2 = sn.con.cursor().execute("select 1")

from snowflake.connector import DictCursor

dcur2 = sn.con.cursor(cursor_class=DictCursor).execute("select 1")

print(df2.equals(df1))                       #> True
print(cur1.fetchone() == cur2.fetchone())    #> True
print(dcur1.fetchone() == dcur2.fetchone())  #> True

cur1 = sn.cursor.execute("select 1")
cur2 = sn.cursor.execute("select 2")

cursor = sn.cursor
cur11 = cursor.execute("select 1")
cur22 = cursor.execute("select 2")

id(cur1) == id(cur2)    #> False
id(cur11) == id(cur22)  #> True

# -- complete example; should run 'as is' --
