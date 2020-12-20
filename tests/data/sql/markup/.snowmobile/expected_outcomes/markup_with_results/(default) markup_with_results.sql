/*: ---------------------------------------------------------------------------
  * This file was stripped of all comments and exported by snowmobile.

  * The tags above each statement either reflect a user-defined tag
    or a tag that was generated in the absence of one.

  * For more information see: https://github.com/GEM7318/snowmobile
--------------------------------------------------------------------------- :*/

/*-
__markup_no_results.sql__
__description***:
This script stores the test cases for `snowmobile.Markup`.
-*/

/*-create-temp table~sample_table-*/
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;

/*-
__intra-statement-marker__
__description: This is a sample intra statement marker.
-*/

/*-select-data~sample select statement-*/
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
