"""
File exists only to map a ``Snowflake`` object to its associated table
within the ``information_schema``.
    -   In all cases except for schemas, this is just adding an `s` to the
        end of the  object (e.g. `table` information in
        ``information_schema.tables``)
    -   In the case of schemas, the associated table is in
        ``information_schema.schemata``
    -   Although the below dictionary contains only a single exception to the
        's' addition, this mapping has been stored in a separate file for
        ease of maintenance/the addition of other objects in the future.

"""
from typing import Dict

MAP_INFORMATION_SCHEMA: Dict[str, str] = {
    "table": "tables",
    "column": "columns",
    "file_format": "file_formats",
    "schema": "schemata",
    "stage": "stages",
    "database": "databases",
    "pipe": "core",
    "procedure": "procedure",
    "function": "functions",
    "external_table": "external_tables",
}
