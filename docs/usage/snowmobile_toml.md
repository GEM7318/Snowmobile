## snowmobile.toml

```{admonition} Tip  
:class: tip
**snowmobile.toml** is a deep set of configuration options.

The intent of this section is to:
   1. Outline how it integrates with {xref}```snowmobile```s API and the best ways to access it 
   2. Store [Field Definitions](#glossary-snowmobiletoml) for reference throughout the rest of the documentation
```

---

### Context

```{eval-rst}
The parsed and validated form of **snowmobile.toml** is a :class:`snowmobile.Configuration` object,
which is accessible as a :class:`Connector` attribute, :attr:`snowmobile.Connector.cfg`.
 
As a convenience, the `delay` keyword argument can be passed to :class:`snowmobile.Connector` which will 
instantiate the object without calling the :meth:`snowflake.connector.connect()` method; this can be verified with:
```

```python
import snowmobile

sn = snowmobile.Connect(delay=True)

sn.alive      #> False
type(sn.con)  #> NoneType

type(sn.cfg)  #> snowmobile.core.configuration.Configuration
str(sn.cfg)   #> snowmobile.Configuration('snowmobile.toml')

print(sn.cfg.location)  #> /path/to/your/snowmobile.toml

sn.cfg.connection.default_alias  #> 'creds1'
```

```{eval-rst}
The API Docs, :mod:`snowmobile.core.cfg` do a better job at articulating the composition
of the object.

Since these two objects come for free with almost every other, most sections map squarely to a 
**snowmobile** object that is intuitively reliant on its contents, which will reference the
below information in the rest of the documentation.
```

```{admonition} Note on *.toml* syntax 
:class: note
- The highest-level parent key of any section is one that includes **zero** unquoted periods; it is at this level
that the parent sections below are broken up into
- See [here](https://github.com/toml-lang/toml) if unfamiliar with *.toml* syntax
```


### Glossary: `snowmobile.toml`

### `[connection]`
This section stores all configuration specs for establishing a connection to the warehouse.

1. **connection**
   - `default-creds`
   - `credentials`
   - `default-arguments` 
2. **loading**
3. **external-sources**
4. **query**
5. **script**
