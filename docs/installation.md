## Getting Started
---

<br>

### 1. Install
`pip install snowmobile`

<br>

### 2. Save *snowmobile.toml*
Download {download}`snowmobile_TEMPLATE.toml <../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml>` and save it in anywhere on your file system as **`snowmobile.toml`**.

<br>

### 3. Store Credentials
The first few lines of [](./usage/snowmobile_toml.md) are outlined below; **for 
minimum configuration,** populate lines 6-12 with a valid set of {xref}`snowflake` 
credentials.

`````{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:class: toggle-shown, sn-indent-h
:language: toml
:lineno-start: 2
:lines: 2-12
:emphasize-lines: 5-12
`````

````{admonition} More Info
:class: note, sn-indent-h, toggle, toggle-shown

`default-creds` on line *3* is an option to specify the connection <u>alias</u> to authenticate with by 
default; if this field is not populated, {xref}`snowmobile` will use the first set of credentials
stored at the level of **connection.credentials** (e.g. `creds1` in this instance).

`creds1` on line *5* is the <u>alias</u> associated with the connection arguments in lines 6-12.
 
See [**Connector: Parameter Resolution**](./usage/connector.md#parameter-resolution) for
detail on what can be included within an aliased credentials block.
````

<br>

### 4. Connect to {xref}`snowflake`

```python
import snowmobile

sn = snowmobile.connect()
```

Successful setup and connection results in ending console output :

    >>>
    Looking for snowmobile.toml in local file system..
    (1 of 1) Located 'snowmobile.toml' at ../Snowmobile/snowmobile.toml
    ..connected: snowmobile.Connector(creds='creds1')

{link-badge}`./usage/connector.html#executing-raw-sql,cls=badge-primary badge text-white,Related: Executing Raw SQL,tooltip=Usage Documentation on Connecting to Snowflake`
{link-badge}`./usage/connector.html#connecting-to-snowflake,cls=badge-warning text-dark,Issues? See Docs,tooltip=Usage Documentation on Connecting to Snowflake`

<hr>

````{admonition} Tip
:class: tip, sn-indent-h
**The rest of the documentation assumes**: 
1.  The first credentials block has been populated with a valid set of credentials
    and its alias remains `creds1`
1.  `default-creds` has been left blank
````
