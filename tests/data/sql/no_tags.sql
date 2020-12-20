-- noinspection SqlResolveForFile

--| create/create or replace schema |------------------------------------------

/*-create-schema~sample_schema-*/
create schema sample_schema
comment = 'Sample Comment';

/*-create-schema~sample_schema-*/
create or replace schema sample_schema
comment = 'Sample Comment';


--| create/create or replace table/transient/temp table |----------------------

/*-create-table~sample_table-*/
create or replace table sample_table as
select 1 as sample_col;

/*-create-temp table~sample_table-*/
create or replace temp table sample_table as
select 1 as sample_col;

/*-create-transient table~sample_table-*/
create or replace transient table sample_table as
select 1 as sample_col;

/*-create-table~sample_table-*/
create table sample_table as
select 1 as sample_col;

/*-create-transient table~sample_table-*/
create transient table sample_table as
select 1 as sample_col;

/*-create-temp table~sample_table-*/
create temp table sample_table as
select 1 as sample_col;


--| create/create or replace table/transient/temp table with CTEs |------------


/*-create-table~sample_table-*/
create or replace table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;

/*-create-transient table~sample_table-*/
create or replace transient table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;

/*-create-temp table~sample_table-*/
create or replace temp table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;

/*-create-table~sample_table-*/
create table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;

/*-create-transient table~sample_table-*/
create transient table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;

/*-create-temp table~sample_table-*/
create temp table sample_table as with
sample_cte as (
	select 1 as sample_col
)
	select
		*
	from sample_cte;


--| create/create or replace table/transient/temp table with DDL |-------------

/*-create-table~sample_table-*/
create or replace table sample_table (
  sample_col varchar(30)
);

/*-create-transient table~sample_table-*/
create or replace transient table sample_table (
  sample_col varchar(30)
);

/*-create-temp table~sample_table-*/
create or replace temp table sample_table (
  sample_col varchar(30)
);

/*-create-table~sample_table-*/
create table sample_table (
  sample_col varchar(30)
);

/*-create-transient table~sample_create_transient_ddl-*/
create transient table sample_create_transient_ddl (
  sample_col varchar(30)
);

/*-create-temp table~sample_create_temp_ddl-*/
create temp table sample_create_temp_ddl (
  sample_col varchar(30)
);


--| drops |--------------------------------------------------------------------

/*-drop-table~sample_table-*/
drop table sample_table;

/*-drop-table~sample_table-*/
drop table if exists sample_table;

/*-drop-schema~sample_schema-*/
drop schema sample_schema;

/*-drop-schema~sample_schema-*/
drop schema if exists sample_schema;


--| selects |------------------------------------------------------------------

/*-select-data~statement-*/
select
	*
from sample_table a;

/*-select-data~statement-*/
select * from sample_table a;

/*-select-data~statement-*/
select count(*) from sample_table d;

/*-select-data~statement-*/
with sample_cte as (
  select * from sample_table st
)
	select
		*
	from sample_cte;


--| updates |------------------------------------------------------------------

/*-update-unknown~statement-*/
update sample_table a
	set a.sample_col = 1
where a.sample_col = 1;


--| inserts |------------------------------------------------------------------

/*-insert-into~statement-*/
insert into sample_table (
  select * from sample_table scort
);


--| deletes |------------------------------------------------------------------

/*-delete-unknown~statement-*/
delete from sample_table a
where  a.sample_col <> 1;



--| sets/unsets |--------------------------------------------------------------

/*-set-param~statement-*/
set sample_param = 1;

/*-set-param~statement-*/
set sample_param = (select max(sample_col) from sample_table);

/*-unset-param~statement-*/
unset sample_param;


--| use schema |---------------------------------------------------------------

/*-use-schema~identifier($schema_name)-*/
use schema identifier($schema_name);
