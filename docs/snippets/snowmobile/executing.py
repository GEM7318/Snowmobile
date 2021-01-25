"""Executing raw sql.
../docs/snippets/executing.py
"""
import snowmobile

sn = snowmobile.connect()

# ================
# -- sn.query() --
df = sn.query("select 1")  #  == pd.read_sql()
type(df)                   #> pandas.core.frame.DataFrame

# -- pd.read_sql() --
import pandas as pd

df2 = pd.read_sql(sql="select 1", con=sn.con)

print(df2.equals(df))  #> True

# =============
# -- sn.ex() --
cur = sn.ex("select 1")    #  == SnowflakeConnection.cursor().execute()
type(cur)                  #> snowflake.connector.cursor.SnowflakeCursor

# -- SnowflakeConnection.cursor().execute() --
cur2 = sn.con.cursor().execute("select 1")

print(cur.fetchone() == cur2.fetchone())  #> True

# ==============
# -- sn.exd() --
dcur = sn.exd("select 1")  #  == SnowflakeConnection.cursor(DictCursor).execute()
type(dcur)                 #> snowflake.connector.DictCursor

# -- SnowflakeConnection.cursor(DictCursor).execute() --
from snowflake.connector import DictCursor

dcur2 = sn.con.cursor(cursor_class=DictCursor).execute("select 1")

print(dcur.fetchone() == dcur2.fetchone())  #> True

# -- complete example; should run 'as is' --
