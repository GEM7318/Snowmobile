
/*-
__markers_duplicates.sql__
__description***: The primary purpose of this script is to test the handling
of duplicate markers within a sql script.

The expected behavior is to detect:
1. *markers_standard.sql*, a leading marker before any statements
1. *markers2.sql*, the first marker between two statements of which a duplicate exists

The third marker is expected to be ignored or throw an error if validation is run
on the script since its contents including the name are identical to the second
marker in the script.
-*/

/*-create table~sample_table-*/
create or replace table sample_table as
select 1 as sample_col;

/*-
__marker2.sql__
__description: second marker
-*/

-- ====/ DUPLICATE /====
/*-
__marker2.sql__
__description: second marker
-*/
-- ====/ DUPLICATE /====
