"""
Setting attributes on a SQL object.
../docs/examples/mod_sql/set_obj_name.py
"""
import snowmobile

# establish a connection, create a temp table
sn = snowmobile.Connector()
sn.query("""
create or replace temp table snowmobile_sample as
select 1 as sample_column;
""")

# query last altered timestamp explicitly providing 'table' argument
query1 = sn.sql.table_last_altered(table='snowmobile_sample', run=False)

# attempt without explicitly providing a 'table' argument
try:
    query2 = sn.sql.table_last_altered()
except ValueError as e:
    print(e)
"""
The value provided for 'table' is not valid, nor is its fallback attribute 'obj_name'.
Please provide a valid value for 'table' or set the 'obj_name' attribute before calling the method.
"""

# set 'obj_name' attribute of SQL object.
sn.sql.obj_name = 'snowmobile_sample'

# method called without providing a 'table' argument
try:
    query2_v2 = sn.sql.table_last_altered(run=False)
except ValueError as e:
    print(e)
"""
"""

# --/ stand-alone example; should run 'as is' /--
