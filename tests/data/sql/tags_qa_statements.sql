
/*-
__script__
__description*: This script houses test cases for QA statements.
-*/

/*-create-temp table~sample_table-*/
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;

/*-qa-empty~verify an expected pass-*/
select
	a.dummy_dim
	,count(*)
from sample_table a
group by 1
having count(*) <> 1;

/*-qa-empty~verify an expected failure-*/
with indistinct_records as (
    select * from sample_table a
  union all
    select * from sample_table a
)
	select
		a.dummy_dim
		,count(*)
	from indistinct_records a
	group by 1
	having count(*) <> 1;

/*-
__name: qa-diff~verify an expected pass (n=2)
__partition-on: 'src_description'
__end-index-at: 'dummy_dim'
__compare-patterns: ['.*_col']
__ignore-patterns: ['.*_exclude']
-*/
with simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from sample_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from sample_table a
)
	select
		*
	from simple_union;

/*-
__name: qa-diff~verify an expected pass (n=3)
__partition-on: src_description
__end-index-at: dummy_dim
__compare-patterns: '.*_col'
__ignore-patterns: '.*_exclude'
-*/
with simple_union as (
  select
    'sample1'
      as src_description
    ,a.*
  from sample_table a
union
  select
    'sample2'
      as src_description
    ,a.*
  from sample_table a
union
  select
    'sample3'
      as src_description
    ,a.*
  from sample_table a
)
	select
		*
	from simple_union;

/*-
__name: qa-diff~verify an expected pass
__partition-on: 'src_description'
__end-index-at: 'idx_col'
__compare-patterns: ['metric']
__ignore-patterns: ['.*_ignore', "ignore.*"]
__absolute-tolerance: 2
-*/
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

/*-
__name: qa-diff~verify an expected pass
__compare-patterns: ['metric']
__ignore-patterns: ['.*_ignore', "ignore.*"]
__end-index-at: 'idx_col'
__absolute-tolerance: 2
__description*: QA-Diff example while omitting arguments:
- `partition_on`
-*/
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

/*-
__name: qa-diff~verify an expected failure
__compare-patterns: ['metric']
__ignore-patterns: ['.*_ignore', "ignore.*"]
__end-index-at: 'idx_col'
__description*: QA-Diff example while omitting arguments:
- `partition_on`
-*/
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

/*-
__name: qa-diff~verify an expected pass
__absolute-tolerance: 2
__description*: QA-Diff example while omitting arguments:
- `partition_on`
- 'end-index-at`
- `compare-patterns`
-*/
with original_testing_table as (
	select 1 as end_index, 1 as metric_diff
union
	select 2 as end_index, 2 as metric_diff
),
altered_testing_table as (
	select 1 as end_index, 2 as metric_diff
union
	select 2 as end_index, 4 as metric_diff
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

/*-
__name: qa-diff~verify an exception is thrown
__partition-on: 'an_invalid_partition_field'
__description*: Omitting all arguments except for intentionally specifying a
`partition-on` column that doesn't exist in the results.
-*/
with original_testing_table as (
	select 1 as end_index, 1 as metric_diff
union
	select 2 as end_index, 2 as metric_diff
),
altered_testing_table as (
	select 1 as end_index, 2 as metric_diff
union
	select 2 as end_index, 4 as metric_diff
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
