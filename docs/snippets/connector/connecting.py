""" Establish a basic connection.
../snippets/intro_connector.py
"""
import snowmobile

sn = snowmobile.connect()

sn2 = snowmobile.connect(creds="creds1")

sn.cfg.connection.current == sn2.cfg.connection.current  #> True
sn.sql.current("schema") == sn2.sql.current("schema")    #> True
sn.sql.current("session") == sn2.sql.current("session")  #> False

# -- complete example; should run 'as is' --
