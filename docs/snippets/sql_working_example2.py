"""
Demonstrate setting attributes on the snowmobile.SQL object in place of
explicitly passing as keyword arguments.
../docs/snippets/sql_working_example2.py
"""
import snowmobile

sn1 = snowmobile.connect()
sn2 = snowmobile.connect()

for sn in [sn1, sn2]:
    sn.sql.auto_run = False

sn1.ex("create transient table sample_table as select 1 as sample_col")

sn2.sql.nm = "sample_table"
sn2.sql.obj = "table"

# -- End Setup ----------------------------------------------------------------

sn1.sql.table_sample(nm="sample_table")
sn2.sql.table_sample()

sn1.sql.columns(nm="sample_table")
sn2.sql.columns()

sn1.sql.columns(nm="sample_table", from_info_schema=True)
sn2.sql.columns(from_info_schema=True)

sn1.sql.ddl(nm="sample_table")
sn2.sql.ddl()

sn1.sql.truncate(nm="sample_table")
sn2.sql.truncate()

sn1.sql.drop(nm="sample_table")
sn2.sql.drop()

# -- End Example --------------------------------------------------------------

sn2.sql.drop(run=True)

# -- End Cleanup --------------------------------------------------------------
