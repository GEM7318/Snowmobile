# markup_no_results.sql

This script stores the test cases for `snowmobile.Markup`.

## (1) create-temp table~sample_table

- **Notes**
	- This is just a sample table for the other test statements to run on.
* Last-Execution
	* **outcome**: _completed_
	* **time**: _1s_

```sql
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;
```

# intra-statement-marker
* **Description**: _This is a sample intra statement marker._

## (2) select-data~sample select statement
* Last-Execution
	* **outcome**: _completed_
	* **time**: _0s_
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
* Last-Execution
	* **outcome**: _passed_
	* **time**: _0s_

```sql
select
	a.dummy_dim
	,count(*)
from sample_table a
group by 1
having count(*) <> 1;
```

## (4) qa-empty~an expected failure
* Last-Execution
	* **outcome**: _failed_
	* **time**: _0s_

```sql
select
	a.dummy_dim
	,count(a.*)
from (select * from sample_table union all select * from sample_table)a
group by 1
having count(*) <> 1;
```

Results
|   dummy_dim |   count(a.*) |
|------------:|-------------:|
|           1 |            2 |
|           2 |            2 |

# Appendix

- This is a sample marker after the last statement in the script.
