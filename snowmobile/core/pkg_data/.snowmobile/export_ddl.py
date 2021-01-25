"""
This file exists for the purpose of exporting DDL.sql to a markdown file.

The relative 'ddl_location' path below assumes that this script is stored
within 'snowmobile/core/pkg_data/.snowmobile' and that `DDL.sql` is in `pkg_data`.
"""
from pathlib import Path

import snowmobile

# location of the DDL.sql file
ddl_location = Path(__file__).absolute().parent.parent / "DDL.sql"

# connector object, connection omitted
sn = snowmobile.connect(delay=True, config_file_nm="snowmobile_testing.toml")

# script object from DDL.sql
script = snowmobile.Script(path=ddl_location, sn=sn)

# accessing as a markup and exporting markdown file only
script.doc().export()
