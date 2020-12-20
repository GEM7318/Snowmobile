
/*-
__DDL.sql__
__description***:
This script stores the default DDL statements utilized by Snowmobile.
- The statement tags include all components (keyword, object, and description) in order to be
able to add additional statements as time progresses without worrying about creating duplicate tag names
	- For clarity, this is why the first statement below is titled _create-file format~snowmobile_default_psv_ as
opposed to just _snowmobile_default_psv_.
-*/

/*-
__name: create-file format~snowmobile_default_psv
__bullets***:
- **Notes**
	- DDL for creating a valid file format associated with the default export-options specified in **snowmobile.toml**
for *snowmobile_default_psv*
	- The only difference between the default *snowmobile_default_psv* and the *snowmobile_default_csv* file
formats is that they are **pipe** and **comma** separated respectively
-*/
create or replace file format snowmobile_default_psv
	file_extension = 'csv'
	field_delimiter = '|'
	compression = gzip
	binary_format = utf8
	date_format = 'yyyy-mm-dd'
	field_optionally_enclosed_by = '\"'
	replace_invalid_characters = true
	trim_space = true
	empty_field_as_null = true
	null_if = ('null', 'null', 'nan', 'NaN', 'None', '\"', '', 'nat');

/*-create-file format~snowmobile_default_csv-*/
create or replace file format snowmobile_default_csv
	file_extension = 'csv'
	field_delimiter = ','
	compression = gzip
	binary_format = utf8
	date_format = 'yyyy-mm-dd'
	field_optionally_enclosed_by = '\"'
	replace_invalid_characters = true
	trim_space = true
	empty_field_as_null = true
	null_if = ('null', 'null', 'nan', 'NaN', 'None', '\"', '', 'nat');

/*-
__Appendix__
__other***:
- See Snowflake's [file format documentation](https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html)
for more information about available format options.
-*/
