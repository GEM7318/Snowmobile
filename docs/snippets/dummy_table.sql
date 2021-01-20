-- ..docs/snippets/dummy_table.sql

create or replace temp table dummy_table as with
sample_data as (
select
  uniform(1, 10, random(1)) as rand_int
from table(generator(rowcount => 5)) v
)
select
    row_number() over (order by a.rand_int) as sample_key
    ,a.rand_int as sample_metric1
    ,uniform(1, 100, random(1)) as sample_metric2
from sample_data a;
