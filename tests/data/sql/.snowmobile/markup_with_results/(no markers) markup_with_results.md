## (1) create-temp table~sample_table


- **Notes**
	- This is just a sample table for the other test statements to run on.
* Execution-Information
	* **Last Outcome**: _completed_

```sql
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;
```

## (2) select data~sample select statement
* Execution-Information
	* **Last Outcome**: _completed_
* **Description**: _This is a sample select statement, including results_

```sql
select * from sample_table;
```

Results
|   dummy_dim |   dummy_exclude |   dummy_col |
|------------:|----------------:|------------:|
|           1 |               1 |           1 |
|           2 |               1 |           1 |

## (3) qa-empty~an expected success
* Execution-Information
	* **Last Outcome**: _passed_

```sql
select
	a.dummy_dim
	,count(*)
from sample_table a
group by 1
having count(*) <> 1;
```

## (4) qa-empty~an expected failure
* Execution-Information
	* **Last Outcome**: _failed_

```sql
select
	a.dummy_dim
	,count(a.*)
from (select * from sample_table union all select * from sample_table)a
group by 1
having count(*) <> 1;
```