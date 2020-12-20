
/*-select-table~',-*/
select get_ddl('table', 'TESTING_SNOWMOBILE.SAMPLE_TABLE') as ddl;

/*-drop-table~testing_snowmobile.sample_table-*/
drop table if exists TESTING_SNOWMOBILE.SAMPLE_TABLE;

/*-248bdb99ecbc37e3bd5836560aa57aab-*/
select
	*
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile';

/*-select-data~statement #4-*/
select
    *
from information_schema.tables
where
	lower(table_name) = 'sample_table'
	and lower(table_schema) = 'testing_snowmobile';

/*-select-data~statement #5-*/
select
table_name
,table_schema
,last_altered
from information_schema.tables
where
lower(table_name) = 'sample_table'
and lower(table_schema) = 'testing_snowmobile';

/*-select-data~statement #6-*/
select
*
from TESTING_SNOWMOBILE.SAMPLE_TABLE
limit 1;
