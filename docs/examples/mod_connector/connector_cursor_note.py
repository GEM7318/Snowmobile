"""
Demonstrate instance/exhaustion component of Connector.cursor.
../examples/mod_connector/connector_cursor_note.py
"""
import snowmobile

sn = snowmobile.Connect()

cur1 = sn.cursor.execute("select 1")
cur2 = sn.cursor.execute("select 2")

cursor = sn.cursor
cur11 = cursor.execute("select 1")
cur22 = cursor.execute("select 2")

id(cur1) == id(cur2)    #> False
id(cur11) == id(cur22)  #> True

# -- freestanding example; should run 'as is' --
