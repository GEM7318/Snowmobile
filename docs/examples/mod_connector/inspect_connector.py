
import snowmobile

sn = snowmobile.Connect()

type(sn)         #> snowmobile.core.connector.Connector

type(sn.cfg)     #> snowmobile.core.configuration.Configuration
str(sn.cfg)      #> snowmobile.Configuration('snowmobile.toml')

type(sn.con)     #> snowflake.connector.connection.SnowflakeConnection
type(sn.cursor)  #> snowflake.connector.cursor.SnowflakeCursor

# -- freestanding example; should run 'as is' --
