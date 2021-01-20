"""
Setting attributes on a SQL object.
../docs/snippets/set_obj_name.py
"""
import snowmobile

sn = snowmobile.connect()  # establish a connection

sn.sql.auto_run = False  # turn off sql.auto_run

sn.query("create temp table demo_table as select 1 as sample_column;")  # demo table


try:
    sql = sn.sql.drop()  # requires table='demo_table'
except ValueError as e:
    raise
# > ValueError: Value provided for 'table' is not valid..

try:
    sn.sql.obj_name = "demo_table"  # set 'obj_name' attribute of SQL object
    sql = sn.sql.drop()  # will now fallback to attribute if omitted
    print(sql)
except ValueError as e:
    raise
# stdout> 'drop table sandbox.DEMO_TABLE'

# -- complete example; should run 'as is' --
