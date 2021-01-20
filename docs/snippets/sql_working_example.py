"""
Demonstrate core functionality of snowmobile.SQL object.
../docs/snippets/sql_working_example.py
"""
import snowmobile

from pathlib import Path

sn = snowmobile.connect()

path = Path.cwd() / "docs/snippets/dummy_table.sql"
_ = snowmobile.Script(path=path, sn=sn).run(1)

# -- 1.1 ----------------------------------------------------------------------

sample1 = sn.sql.table_sample("dummy_table", n=5)

print(type(sample1))  #> <class 'pandas.core.frame.DataFrame'>
print(sample1.shape)  #> (5, 3)

sample1_run_false = sn.sql.table_sample("dummy_table", n=5, run=False)

print(type(sample1_run_false))  #> <class 'str'>
print(sample1_run_false)

# -- 1.2 ----------------------------------------------------------------------

sn.sql.auto_run = False

sample2 = sn.sql.table_sample("dummy_table", n=5)

print(type(sample2))                 #> <class 'str'>
print(sample2 == sample1_run_false)  #> True

sample2_run_true = sn.sql.table_sample("dummy_table", n=5, run=True)

print(type(sample2_run_true))            #> <class 'pandas.core.frame.DataFrame'>
print(sample2_run_true.equals(sample1))  #> True

# -- complete example; should run 'as is' --
