
/*-
__script__
__description*: Script houses test cases for QA statements.
-*/

/*-set param~schema_name-*/
set schema_name = 'snowmobile_testing';

/*-create schema~#2-*/
create or replace schema identifier($schema_name)
comment = 'Sample cfg script';

/*-use schema~#3-*/
use schema identifier($schema_name);

/*-create table~snowmobile_testing.sample_table-*/
create or replace temp table snowmobile_testing.sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;

/*-select data~snowmobile_testing.sample_table-*/
select
	*
from snowmobile_testing.sample_table st;

/*-qa-empty~verify sample_table is distinct on dummy_dim-*/
select
	a.dummy_dim
	,count(*)
from snowmobile_testing.sample_table a
group by 1
having count(*) <> 1;

/*-
__name: select data~results testing
__description*: Test of inserting results.
__another-bullet: This is a bullet
__results*: true
-*/
select * from snowmobile_testing.sample_table st;

/*-
__name: select data~results testing2
__description*: *Note*: This is a paragraph
__results*_***: true
-*/
select * from snowmobile_testing.sample_table st;

/*-
__name: select data~results testing3
__results*_***: true
__sql*_***: true
-*/
select * from snowmobile_testing.sample_table st;

/*-
__name: select data~results testing4
__sql*_***: true
__results*_***: true
-*/
select * from snowmobile_testing.sample_table st;

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

/*-custom1-select~sample customer-*/
select 1;


/*-
__name: qa-diff~verify two things we know are equal are actually equal
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

/*-
__name: qa-diff~verify three things we know are equal are actually equal
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


/*-
__name: qa-diff~something that should throw an error for no compare or drop columns
__partition-on: 'src_description'
__end-index-at: 'idx_col'
__compare-patterns: ['.*metric']
__absolute-tolerance: 0
__relative-tolerance: 1
-*/
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


/*-
__name: qa-diff~compare two things with a relative tolerance of 1
__partition-on: 'src_description'
__end-index-at: 'idx_col'
__compare-patterns: ['metric']
__ignore-patterns: ['.*_ignore', "ignore.*",'dummy pattern']
__relative-tolerance: 0.49
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


/* statement without a tag */
select * from snowmobile_testing.sample_table st;

/*-drop-schema~snowmobile_testing-*/
drop schema if exists snowmobile_testing;
