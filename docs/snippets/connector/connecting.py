""" Establish a basic connection.
../docs/snippets/connecting.py
"""
import snowmobile

sn = snowmobile.connect()

print(sn)            #> snowmobile.Connector(creds='creds1')
print(sn.cfg)        #> snowmobile.Configuration('snowmobile.toml')
print(type(sn.con))  #> <class 'snowflake.connector.connection.SnowflakeConnection'>

sn2 = snowmobile.connect(creds="creds1")

sn.cfg.connection.current == sn2.cfg.connection.current  #> True
sn.sql.current("schema") == sn2.sql.current("schema")    #> True
sn.sql.current("session") == sn2.sql.current("session")  #> False

# -- complete example; should run 'as is' --
