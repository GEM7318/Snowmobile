
/*-
__markup_no_results.sql__
__description***:
This script stores the test cases for `snowmobile.Markup`.
-*/

/*-
__name: create-temp table~sample_table
__bullets***:
- **Notes**
	- This is just a sample table for the other test statements to run on.
-*/
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;

/*-
__intra-statement-marker__
__description: This is a sample intra statement marker.
-*/

/*-
__name: select data~sample select statement
__description: This is a sample select statement, including results
__results*: true
-*/
select * from sample_table;

/*-qa-empty~an expected success-*/
select
	a.dummy_dim
	,count(*)
from sample_table a
group by 1
having count(*) <> 1;

/*-qa-empty~an expected failure-*/
select
	a.dummy_dim
	,count(a.*)
from (select * from sample_table union all select * from sample_table)a
group by 1
having count(*) <> 1;

/*-
__Appendix__
__other***:
- This is a sample marker after the last statement in the script.
-*/
