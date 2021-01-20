"""
Instantiate a delayed snowmobile.Connector object.
../docs/snippets/instantiate_connector.py
"""

import snowmobile

sn = snowmobile.Connector(delay=True)

type(sn)                  #> snowmobile.core.connector.Connector
type(sn.con)              #> None

type(sn.cfg)              #> snowmobile.core.configuration.Configuration
print(sn.cfg.location)    #  'path/to/your/snowmobile.toml'

type(sn.cfg.connection)   #> snowmobile.core.cfg.connection.Connection
type(sn.cfg.loading)      #> snowmobile.core.cfg.loading.Loading
type(sn.cfg.script)       #> snowmobile.core.cfg.script.Script
type(sn.cfg.sql)          #> snowmobile.core.cfg.other.SQL
type(sn.cfg.ext_sources)  #> snowmobile.core.cfg.other.Location

# -- complete example; should run 'as is' --
