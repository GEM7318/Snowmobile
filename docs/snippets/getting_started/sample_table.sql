-- noinspection SqlResolveForFile
-- ..docs/snippets/example/sample_table.sql

select * from sample_table;

create transient table any_table as
select
	a.*
from sample_table a
where
	a.col2 = 0;
select
  count(*)
from any_table;

insert into any_other_table (
  select
		row_number() over (order by a.col1)
       as index
    ,a.col1
    ,a.col2
    ,a.loaded_tmstmp
      as staged_tmstmp
    ,current_timestamp()
      as insert_tmstmp
  from sample_table a
);

/*-qa-empty~ensure 'any_other_table' is distinct on 'col1'-*/
select
  a.index
	,count(*)
from any_other_table a
group by 1
having count(*) > 1;

drop table any_table;
drop table sample_table;
