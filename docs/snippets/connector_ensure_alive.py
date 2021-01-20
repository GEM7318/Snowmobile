"""
Demonstrate behavior of Connector's 'ensure_alive' parameter.
..docs/snippets/connector_ensure_alive.py
"""
import snowmobile

# --- SESSION #1 ---

# Explicitly providing default argument for clarity
sn = snowmobile.connect(ensure_alive=True)

print(sn.alive)  #> True
type(sn.con)     #> snowflake.connector.connection.SnowflakeConnection

# Storing 1st session ID
session1 = sn.sql.current('session')

# Killing connection
sn.disconnect()

print(sn.alive)  #> False
type(sn.con)     #> NoneType

# --- SESSION #2 ---

# Calling any method requiring a connection
_ = sn.query("select 1")

# Storing 2nd session ID
session2 = sn.sql.current('session')

# Verifying both session IDs are valid
print(type(session1))  #> str
print(type(session2))  #> str

# Verifying they're unique
print(session1 != session2)  #> True

# -- complete example; should run 'as is' --
