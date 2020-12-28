
/*-
__markers_standard.sql__
__description***: The primary purpose of this script is to test the most basic
of marker functionality.

The expected behavior is to detect:
1. *markers_standard.sql*, a leading marker before any statements
1. *markers2.sql*, a marker between two statements
1. *markers3.sql*, a second consecutive marker between two statements
1. *trailing_marker*, a trailing marker after all statements

__secondary***: The secondary purpose of this script is to test the re-indexing
of statements and markers.

The behavior expected is for the script to containing the following objects/order:
1. Marker(`markers_standard.sql')
2. Statement(`create-table~sample_table')
3. Marker(`marker2')
4. Marker(`marker3')
5. Statement(`create-table~sample_table')
6. Marker('trailing_marker')
-*/

/*-create table~sample_table-*/
create or replace table sample_table as
select 1 as sample_col;

/*-
__marker2__
__description: second marker
-*/

/*-
__marker3__
__description: third marker in total, second consecutive marker between two
statements.
-*/

/*-create table~sample_table2-*/
create or replace table sample_table2 as
select 1 as sample_col;

/*-
__trailing_marker__
__description: This is a trailing marker.
-*/
