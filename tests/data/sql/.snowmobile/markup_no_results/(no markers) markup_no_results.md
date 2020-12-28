## (1) create temp table~sample_table


- **Notes**
	- This is just a sample table for the other test statements to run on.

```sql
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;
```

## (2) select data~sample select statement
* **Description**: _This is a sample select statement, excluding results_

```sql
select * from sample_table;
```