## snowmobile.Connector

### .Connect()
Let's start by establishing a new connection.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 1
:lines: 1-7
```

This **snowmobile.Connector** object, `sn` hereafter, includes the standard Snowflake `Connector`as part of
**snowmobile**'s object model.

The below snippet outlines the attributes of `sn` touched on so far:
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 9
:lines: 9-15
```

The `sn` object re-implements several forms query execution to minimize verbosity as well
as make the two most common forms of querying available from the same method.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 17
:lines: 17-21
```

`sn.con: SnowflakeConnection` is left as a public attribute so that its internal methods remain available
and so that it can be passed to other libraries directly off the **snowmobile.Connector** object.

As a somewhat contrived example of this, the below statements use `sn.con` to create *df2* and *cur2* objects
with methods from Pandas and Snowflake respectively, the contents of which  mirror *df1* and *cur1*
created by `sn.query()` above.
```{literalinclude} /examples/setup/quick_intro_connector.py
:language: python
:lineno-start: 23
:lines: 23-29
```

The full script for this section can be found [here](../examples.md#quick-intro-snowmobileconnector)
