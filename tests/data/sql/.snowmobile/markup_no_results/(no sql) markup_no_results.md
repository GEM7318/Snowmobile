# markup_no_results.sql


This script stores the test cases for `snowmobile.Markup`.

## (1) create temp table~sample_table


- **Notes**
	- This is just a sample table for the other test statements to run on.

```sql
create or replace temp table sample_table as
	select 1 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col
union
	select 2 as dummy_dim, 1 as dummy_exclude, 1 as dummy_col;
```

# intra-statement-marker
* **Description**: _This is a sample intra statement marker._

## (2) select data~sample select statement
* **Description**: _This is a sample select statement, excluding results_

```sql
select * from sample_table;
```

# Appendix


- This is a sample marker after the last statement in the script.