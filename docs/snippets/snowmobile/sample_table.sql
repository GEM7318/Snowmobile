-- ..docs/snippets/snowmobile/sample_table.sql

/*-create transient table~any_random_table1-*/
create or replace transient table any_random_table1 (
	rand_col1 int
);

/*-create table~sample_table-*/
create or replace table sample_table (
	col1 int,
	col2 int
);

select * from any_random_table1;

/*-select data~sample_table-*/
select * from sample_table;
