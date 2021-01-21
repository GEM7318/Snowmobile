## Setup
---

<br>

### 1. Install
`pip install snowmobile`

<br>

### 2. Save *snowmobile.toml*
Download {download}`snowmobile_TEMPLATE.toml <../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml>` 
and save it in anywhere on your file system as **`snowmobile.toml`**.
+++
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
`````

````{admonition} More Info
:class: note, toggle, sn-indent-h, sn-dedent-h-t

On line *3*, `default-creds` represents the *alias* associated
with the connection arguments to authenticate with by default if one is not passed 
to the *creds* argument of {meth}`snowmobile.connect()`.
 
In instances where this field is left empty and an alias is not explicitly
provided to {meth}`~snowmobile.Connector.connect()`, the first set of 
credentials stored at the level of **`connection.credentials.*`** will be 
used (e.g. `creds1` above).

<hr class="sn-blue">

On line *5*, `creds1` is the <u>alias</u> associated with the connection arguments in lines 6-12.

For granular information on what can be included within an aliased credentials block, see
[**Connector: Parameter Resolution**](./usage/connector.md#parameter-resolution).
````

<br>

### 4. Connect to {xref}`snowflake`
Successful setup and connection can be verified with:
```python
import snowmobile

sn = snowmobile.connect()
```
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
