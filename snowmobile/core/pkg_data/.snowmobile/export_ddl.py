"""
This file exists for the purpose of exporting DDL.sql to a markdown file.

The relative 'ddl_location' path below assumes that this script is stored
within '/pkg_data/.snowmobile'.
"""
from pathlib import Path
import snowmobile

# location of the DDL.sql file
ddl_location = Path(__file__).absolute().parent.parent / "DDL.sql"
# ddl_location = Path(r'C:\Users\GEM7318\Documents\Github\Snowmobile\snowmobile\core\pkg_data\DDL.sql')

# connector object, connection omitted
sn = snowmobile.Connect(delay=True)

# script object from DDL.sql
script = snowmobile.Script(path=ddl_location, sn=sn)

# accessing as a markup and exporting markdown file only
script.doc().export()
# doc = script.doc()
# doc.export(sql_only=True)
# doc.exported
