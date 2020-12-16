
# qa_statements.sql
* Author-Information
	* **Team**: _Pizza Hut U.S. Data Science_
	* **Full Name**: _Grant Murray_
	* **Internal ID**: gem7318
	* **Email**: _grant.murray@yum.com_


## (1) qa-empty~verify sample_table is distinct on dummy_dim
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _passed_

SQL
```sql
select
	a.dummy_dim
	,count(*)
from snowmobile_testing.sample_table a
group by 1
having count(*) <> 1;
```



## (2) qa-empty~an intentional failure
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _failed_

SQL
```sql
with indistinct_records as (
    select * from snowmobile_testing.sample_table a
  union all
    select * from snowmobile_testing.sample_table a
)
	select
		a.dummy_dim
		,count(*)
	from indistinct_records a
	group by 1
	having count(*) <> 1;
```



## (3) qa-diff~verify two things we know are equal are actually equal
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _passed_
* QA-Specifications
	* **Partition-On**: _src_description_
	* **End-Index-At**: _dummy_dim_
	* **Compare-Patterns**: _['.*_col']_
	* **Ignore-Patterns**: _['.*_exclude']_

SQL
```sql
with simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from snowmobile_testing.sample_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from snowmobile_testing.sample_table a
)
	select
		*
	from simple_union;
```



## (4) qa-diff~verify three things we know are equal are actually equal
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _passed_
* QA-Specifications
	* **Partition-On**: _src_description_
	* **End-Index-At**: _dummy_dim_
	* **Compare-Patterns**: _['.*_col']_
	* **Ignore-Patterns**: _['.*_exclude']_

SQL
```sql
with simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from snowmobile_testing.sample_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from snowmobile_testing.sample_table a
union
  select
    'sample3'
      as src_description
    ,a.*
  from snowmobile_testing.sample_table a
)
	select
		*
	from simple_union;
```



## (5) qa-diff~something that should throw an error for no compare or drop columns
* **Absolute-Tolerance**: _0.0_
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _failed_
* QA-Specifications
	* **Partition-On**: _src_description_
	* **End-Index-At**: _idx_col_
	* **Compare-Patterns**: _['.*metric']_
	* **Relative-Tolerance**: _1.0_

SQL
```sql
with original_testing_table as (
	select 1 as idx_col, 1 as metric
union
	select 2 as idx_col, 2 as metric
),
altered_testing_table as (
	select 1 as idx_col, 2 as metric
union
	select 2 as idx_col, 4 as metric
),
simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from original_testing_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from altered_testing_table a
)
	select
		*
	from simple_union;
```



## (6) qa-diff~compare two things with a relative tolerance of 1
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _failed_
* QA-Specifications
	* **Partition-On**: _src_description_
	* **End-Index-At**: _idx_col_
	* **Compare-Patterns**: _['metric']_
	* **Ignore-Patterns**: _['.*_ignore', 'ignore.*', 'dummy pattern']_
	* **Relative-Tolerance**: _0.49_

SQL
```sql
with original_testing_table as (
	select 1 as idx_col, 1 as metric, 3 as sample_ignore, 4 as ignore_other
union
	select 2 as idx_col, 2 as metric, 3 as sample_ignore, 4 as ignore_other
),
altered_testing_table as (
	select 1 as idx_col, 2 as metric, 3 as sample_ignore, 4 as ignore_other
union
	select 2 as idx_col, 4 as metric, 3 as sample_ignore, 4 as ignore_other
),
simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from original_testing_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from altered_testing_table a
)
	select
		*
	from simple_union;
```
