-- noinspection SqlResolveForFile

/*-1-*/
select
	*
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile';

/*-2-*/
select
	*
from information_schema.columns
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile';

/*-3-*/
select
	table_name
	,table_schema
	,last_altered
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile';

/*-4-*/
select
	*
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'other_schema';

/*-5-*/
select
	*
from information_schema.columns
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'other_schema';

/*-6-*/
select
	table_name
	,table_schema
	,last_altered
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'other_schema';

/*-7-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_TABLE;

/*-8-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_VIEW;

/*-9-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_SCHEMA;

/*-10-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_WAREHOUSE;

/*-11-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_DATABASE;

/*-12-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_TABLE;

/*-13-*/
drop view if exists TESTING_SNOWMOBILE.SAMPLE_VIEW;

/*-14-*/
drop schema if exists SAMPLE_SCHEMA;

/*-15-*/
drop warehouse if exists SAMPLE_WAREHOUSE;

/*-16-*/
drop database if exists SAMPLE_DATABASE;

/*-17-*/
drop table if exists OTHER_SCHEMA.OTHER_TABLE;

/*-18-*/
drop table if exists DEFAULT_SCHEMA.OTHER_TABLE;

/*-19-*/
drop table if exists OTHER_SCHEMA.OTHER_TABLE;

/*-20-*/
drop table if exists OTHER_SCHEMA.DEFAULT_TABLE;

/*-21-*/
drop view if exists DEFAULT_SCHEMA.OTHER_VIEW;

/*-22-*/
drop view if exists OTHER_SCHEMA.OTHER_VIEW;

/*-23-*/
select current_schema();

/*-24-*/
select current_database();

/*-25-*/
select current_warehouse();

/*-26-*/
select current_role();

/*-27-*/
use schema EXAMPLE_SCHEMA;

/*-28-*/
use database EXAMPLE_DATABASE;

/*-29-*/
use warehouse EXAMPLE_WAREHOUSE;

/*-30-*/
use role EXAMPLE_ROLE;

/*-31-*/
select
*
from TESTING_SNOWMOBILE.SAMPLE_TABLE
limit 1;

/*-32-*/
select
	ordinal_position
	,column_name
from information_schema.columns
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile'
order by 1;
