## snowmobile.toml

```{admonition} Tip 
:class: hint
- **snowmobile.toml** is a deep set of configuration options and not one that should be consumed
all at once
- The below information is best served as a reference throughout the rest of the documentation and
on an as-needed basis as one becomes more familiar with the composition of **snowmobile**'s objects
```

---

### Context

**snowmobile.toml** is ground zero for `snowmobile`'s object model and is referenced heavily
throughout the documentation.

Except for some inherent crossover of certain sections (e.g. requiring `[credentials]` to execute 
any command against Snowflake), most sections map squarely to a **snowmobile** object that most 
heavily leverages its associated configuration options. 

```{eval-rst}
The parsed and validated form of **snowmobile.toml** is a :class:`snowmobile.Configuration` object,
which is accessible as a :class:`snowmobile.Connector` attribute, :attr:`snowmobile.Connector.cfg`. 

It is intentional across the entire object model that the configuration & credentials
are paired with :class:`snowmobile.Connector`, being the object that executes commands against Snowflake.

The practical application of this will become significantly more clear with the examples starting in the next section. 
```

```{admonition} Note on *.toml* syntax 
:class: note
- The highest-level parent key of any section is one that includes **zero** unquoted periods; it is at this level
that the parent sections below are broken up into
- See [here](https://github.com/toml-lang/toml) if unfamiliar with *.toml* syntax
```

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
