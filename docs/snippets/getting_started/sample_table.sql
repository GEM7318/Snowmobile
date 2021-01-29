-- noinspection SqlResolveForFile
-- ..docs/snippets/getting_started/sample_table.sql

create or replace table sample_table (
	col1 number(18,0),
	col2 number(18,0)
);

insert into sample_table with
sample_data as (
  select
    uniform(1, 10, random(1)) as rand_int
  from table(generator(rowcount => 3)) v
)
  select
    row_number() over (order by a.rand_int) as col1
    ,(col1 * col1) as col2
  from sample_data a;

select * from sample_table;

/*-qa-empty~verify 'sample_table' is distinct on 'col1'-*/
select
  a.col1
  ,count(*)
from sample_table a
group by 1
having count(*) <> 1;

/*-insert into~any_other_table-*/
insert into any_other_table (
  select
    a.*
    ,tmstmp.tmstmp as insert_tmstmp
  from sample_table a
  cross join (select current_timestamp() as tmstmp)tmstmp
);
