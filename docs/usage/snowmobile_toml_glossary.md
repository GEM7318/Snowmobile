## Glossary

(connection)=
```{tabbed} [connection]
:new-group:
    
*Groups all configuration options for establishing connections to {xref}`snowflake`*
```

(default-creds)=
```{tabbed} default-creds
:new-group:

*The credentials *alias* to use by default if not specified.*
```    

(connection.credentials.creds1)=    
```{tabbed} [connection.credentials.creds1]
:new-group:

*Filler space for a first set of credentials.*
``` 

(connection.credentials.creds2)=    
```{tabbed} [connection.credentials.creds2]
:new-group:

*Filler space for a second set of credentials.*
```

(connection.credentials)=
```{tabbed} [connection.credentials]
:new-group:
    
*Groups subsections of credentials, each declared with the structure of ``[connection.credentials.credentials_alias]``*
```

```{tabbed} +
    
The value of `credentials_alias` is the literal string to pass to the ``creds`` argument of {class}`snowmobile.Connector` to establish 
the {xref}`snowflake` connection with those credentials.

Additional keyword-arguments can be specified in an aliased section so long as they are provided **verbatim** as they should be 
passed to the {meth}`snowflake.connector.connect()` method; this can be used to to map a specific timezone or transaction mode (for example) 
to a specific set of credentials.
```

(connection.default-arguments)=
```{tabbed} [connection.default-arguments]
:new-group:
   
*Arguments to include with every connection*
```

```{tabbed} +

Any arguments in this section that overlap with those stored in an aliased credentials block will be superceded by those associated with the credentials.

```
