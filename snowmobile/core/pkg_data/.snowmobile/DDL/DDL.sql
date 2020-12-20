/*: ---------------------------------------------------------------------------
  * This file was stripped of all comments and exported by snowmobile.

  * The tags above each statement either reflect a user-defined tag
    or a tag that was generated in the absence of one.

  * For more information see: https://github.com/GEM7318/snowmobile
--------------------------------------------------------------------------- :*/

/*-
__DDL.sql__
__description***:
This script stores the default DDL statements utilized by Snowmobile.
- The statement tags include all components (keyword, object, and description) in order to be
able to add additional statements as time progresses without worrying about creating duplicate tag names
	- For clarity, this is why the first statement below is titled _create-file format~snowmobile_default_psv_ as
opposed to just _snowmobile_default_psv_.
-*/

/*-create-file format~snowmobile_default_psv-*/
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
