## Setup
---

<br>

**1. Installation**

`pip install snowmobile`

<br>

**2. Save a snowmobile.toml file**

````{tabbed} Download
```{only} builder_html
Download {download}`this <../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml>` file and
remove the `_TEMPLATE` portion of the file name so that it's saved as **snowmobile.toml**.
```
````

````{tabbed} Copy File Contents
Copy the contents below in a file called **snowmobile.toml** anywhere on your local file
system.
```{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 1
```
````

<br>

**3. Store A Set Credentials**

The first few lines of **snowmobile.toml** are outlined below; **for minimum configuration**:
1. Specify a valid set of credentials within the **[connection.credentials.creds1]** block
1. Modify or remove any unwanted arguments within the **[connection.default-arguments]** block

````{literalinclude} ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
:language: toml
:lineno-start: 2
:lines: 2-26
:emphasize-lines: 4, 13, 22
````

```{note}
For initial setup and to ensure replicability of code samples, it's a good idea to:
1.  Leave *default-creds* as is
1.  Leave the **aliases** for *creds1* and *creds2* as *creds1* and *creds2*
1.  Store a second set of credentials under *creds2* if available; if not, store the same set as used
    for *creds1* under the alias *creds2* as well
```

<br>

**4. Connect to** {xref}`snowflake`

```python
import snowmobile

sn = snowmobile.connect()
```

Successful setup and connection results in ending console output similar to:

    >>>
    Looking for snowmobile.toml in local file system..
    (1 of 1) Located 'snowmobile.toml' at ../Snowmobile/snowmobile.toml
    ..connected: snowmobile.Connector(creds='creds1')

{link-badge}`./usage/connector.html#executing-raw-sql,cls=badge-primary badge text-white,Related: Executing Raw SQL,tooltip=Usage Documentation on Connecting to Snowflake`
{link-badge}`./usage/connector.html#connecting-to-snowflake,cls=badge-warning text-dark,Issues? See Docs,tooltip=Usage Documentation on Connecting to Snowflake`

<br>