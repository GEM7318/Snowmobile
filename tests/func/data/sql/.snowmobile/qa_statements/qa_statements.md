
# qa_statements.sql
* Author-Information
	* **Team**: _Pizza Hut U.S. Data Science_
	* **Full Name**: _Grant Murray_
	* **Internal ID**: gem7318
	* **Email**: _grant.murray@yum.com_


## (1) set-param~schema_name
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
set schema_name = 'snowmobile_testing';
```



## (2) create-schema~#2
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
create or replace schema identifier($schema_name)
comment = 'Sample schema script';
```



## (3) use-schema~#3
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
use schema identifier($schema_name);
```



## (4) create-table~snowmobile_testing.sample_table
* Execution-Information
	* **Execution Time**: _1s_
	* **Last Outcome**: _completed_

SQL
```sql
create or replace temp table snowmobile_testing.sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;
```



## (5) select-data~snowmobile_testing.sample_table
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
select
	*
from snowmobile_testing.sample_table st;
```



## (6) qa-empty~verify sample_table is distinct on dummy_dim
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



## (7) select-data~results testing
* **Another-Bullet**: _This is a bullet_
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

**Description**
_Test of inserting results._

SQL
```sql
select * from snowmobile_testing.sample_table st;
```


Results
|   dummy_dim |   dummy_exclude |   dummy_col |
|------------:|----------------:|------------:|
|           1 |               1 |           1 |
|           2 |               1 |           1 |


## (8) select-data~results testing2
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

**Description**
_*Note*: This is a paragraph_

SQL
```sql
select * from snowmobile_testing.sample_table st;
```


|   dummy_dim |   dummy_exclude |   dummy_col |
|------------:|----------------:|------------:|
|           1 |               1 |           1 |
|           2 |               1 |           1 |


## (9) select-data~results testing3
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

```sql
select * from snowmobile_testing.sample_table st;
```


|   dummy_dim |   dummy_exclude |   dummy_col |
|------------:|----------------:|------------:|
|           1 |               1 |           1 |
|           2 |               1 |           1 |


## (10) select-data~results testing4
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

```sql
select * from snowmobile_testing.sample_table st;
```


|   dummy_dim |   dummy_exclude |   dummy_col |
|------------:|----------------:|------------:|
|           1 |               1 |           1 |
|           2 |               1 |           1 |


## (11) qa-empty~an intentional failure
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



## (12) custom1-select~sample customer
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
select 1;
```



## (13) qa-diff~verify two things we know are equal are actually equal
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



## (14) qa-diff~verify three things we know are equal are actually equal
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



## (15) qa-diff~something that should throw an error for no compare or drop columns
* **Absolute-Tolerance**: _0.0_
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _passed_
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



## (16) qa-diff~compare two things with a relative tolerance of 1
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



## (17) select-data~statement #17
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
select * from snowmobile_testing.sample_table st;
```



## (18) drop-schema~snowmobile_testing
* Execution-Information
	* **Execution Time**: _0s_
	* **Last Outcome**: _completed_

SQL
```sql
drop schema if exists snowmobile_testing;
```
