"""
Alter default behavior of SQL.auto_run=True
../docs/examples/mod_sql/set_auto_run.py
"""
import snowmobile

# connector, omitting unnecessary connection for example
sn = snowmobile.Connector(delay=True)

# default requires `run=False` to store sql without executing
sql1 = sn.sql.use_schema(nm='other_schema', run=False)

# setting auto_run=False on the contained SQL object
sn.sql.auto_run = False

# `run=False` no longer needed
sql2 = sn.sql.use_schema(nm='other_schema')

print(sql1 == sql2)
# console> True

# --/ stand-alone example; should run 'as is' /--
