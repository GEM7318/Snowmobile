```{include} /badges.md
```
<hr style="margin-top: -0.2rem;">

{xref}`snowmobile` bundles the {xref}`SnowflakeConnection` into an object model focused on configuration-management
and making it easy to work with {xref}`snowflake` in natural, idiomatic Python.

**Its main features are:**
<style>
truncated {
    margin: 0 0.1rem 0.1rem 1.1rem;
}
</style>
<DL style="margin-top: -0.4em;">
<DT><span class="fa fa-check text-success mr-1"></span><a class="reference internal" href="usage/snowmobile_toml.html#snowmobile-toml"><span class="std std-doc">Consolidated configuration: snowmobile.toml</span></a>
    <dd class="truncated">Use one configuration file, tracked by <a class="reference external" href="https://pypi.org/project/snowmobile/">snowmobile</a> and accessible from all Python instances on a machine

<DT><span class="fa fa-check text-success mr-1"></span><a class="reference internal" href="usage/connector.html#executing-raw-sql"><span class="std std-doc">Simplified execution of raw SQL</span></a>
    <dd class="truncated">Query results into a <a class="reference external" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html">DataFrame</a>, 
    <a class="reference external" href="https://docs.snowflake.com/en/user-guide/python-connector-api.html#cursor">SnowflakeCursor</a> or 
    <a class="reference external" href="https://docs.snowflake.com/en/user-guide/python-connector-api.html#cursor">DictCursor</a> from the same object

<DT><span class="fa fa-check text-success mr-1"></span><a class="reference internal" href="usage/table.html"><span class="std std-doc">Refined data loading implementation</span></a>
    <dd class="truncated">DDL from <a class="reference external" href="https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html">DataFrame</a>;
    compatibility checks at run time; supports <i>if_exists</i> in (<i>'truncate'</i>, <i>'append'</i>, <i>'replace'</i>, <i>'fail'</i>)

<DT><span class="fa fa-check text-success mr-1"></span><a class="reference internal" href="usage/script.html#examples"><span class="std std-doc">.sql scripts as Python objects</span></a>
    <dd class="truncated">Scripts as context managers; work with actual statements; add markup; export to markdown
</DL>

```{note} 
{xref}`snowmobile` is a wrapper **around** the {xref}`snowflake.connector2`, 
not a replacement for it; the {xref}`SnowflakeConnection` is intentionally
stored as a public attribute so that the {xref}`snowflake.connector2` 
and {xref}`snowmobile` APIs can be leveraged congruently. 
```

<hr style="margin: 0;">
