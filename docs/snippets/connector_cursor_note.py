"""
Demonstrate instance/exhaustion component of Connector.cursor.
../snippets/connector_cursor_note.py
"""
import snowmobile

sn = snowmobile.connect()

cur1 = sn.cursor.execute("select 1")
cur2 = sn.cursor.execute("select 2")

cursor = sn.cursor
cur11 = cursor.execute("select 1")
cur22 = cursor.execute("select 2")

id(cur1) == id(cur2)    #> False
id(cur11) == id(cur22)  #> True

# -- complete example; should run 'as is' --
