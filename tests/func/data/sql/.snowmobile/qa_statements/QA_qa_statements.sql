
/*: ---------------------------------------------------------------------------
  * This file was stripped of all comments and exported by snowmobile.

  * The tags above each statement either reflect a user-defined tag
    or a tag that was generated in the absence of one.

  * For more information see: https://github.com/GEM7318/snowmobile
--------------------------------------------------------------------------- :*/

/*-
__script__
__author-information: {'team': 'Pizza Hut U.S. Data Science', 'Full Name': 'Grant Murray', '\\*\\*Internal ID\\*\\***': 'gem7318', 'email': 'grant.murray@yum.com'}
-*/

/*-qa-empty~verify sample_table is distinct on dummy_dim-*/
select
	a.dummy_dim
	,count(*)
from snowmobile_testing.sample_table a
group by 1
having count(*) <> 1;

/*-qa-empty~an intentional failure-*/
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

/*-qa-diff~verify two things we know are equal are actually equal-*/
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

/*-qa-diff~verify three things we know are equal are actually equal-*/
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

/*-qa-diff~something that should throw an error for no compare or drop columns-*/
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

/*-qa-diff~compare two things with a relative tolerance of 1-*/
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

