---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.4.1
  kernelspec:
    display_name: snowmobile2
    language: python
    name: snowmobile2

orphan: true
---

```python tags=["remove-cell"]
import sys

from pathlib import Path

for p in [
#     r'C:\Users\GEM7318\Documents\Github\Snowmobile',
    r'C:\Program Files\JetBrains\PyCharm 2019.3.4\plugins\python\helpers\pycharm_matplotlib_backend',
    r'C:\Users\GEM7318\Anaconda3\envs\snowmobile2\lib\site-packages\IPython\extensions',
    r'C:\Users\GEM7318\Anaconda3\envs\snowmobile2',
    r'C:\Users\GEM7318\Anaconda3\envs\snowmobile2\lib',
    r'C:\Users\GEM7318\Anaconda3\envs\snowmobile2\lib\site-packages',
]:
    sys.path.append(p)
```

```python tags=["remove-cell"]
import os
os.chdir(str(Path.cwd().parent.parent))
```

<!-- #region tags=["remove-cell"] -->
------
---
------
---
---
<!-- #endregion -->

## Example


Establishing a connection through {class}`snowmobile.Snowmobile`

```python
import snowmobile

sn = snowmobile.connect()
```

Then given a {xref}`DataFrame` like this:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame(
    data = {'col1': np.ones(3), 'col2': np.zeros(3)}
)
df.head(2)
```

```python tags=["remove-cell"]
if sn.sql.exists('sample_table'):
    sn.sql.drop('sample_table')
```

Loading to a table with {class}`snowmobile.Table`

```python tags=["remove-output"]
snowmobile.Table(sn=sn, df=df, table='sample_table').load()
```

Verifying load with {class}`snowmobile.SQL`

```python
sn.sql.exists('sample_table')
```

Querying table with {class}`~snowmobile.Snowmobile`..


Into a {xref}`DataFrame`

```python
sn.query('select * from sample_table')
```

Also into an {xref}`SnowflakeCursor`

```python
sn.ex('select * from sample_table').fetchall()
```

```python
print(sn.sql.ddl('sample_table'))
```

```python tags=["remove-output"]
snowmobile.Table(
    sn=sn,
    df=df,
    table='sample_table',
    if_exists='append',
    as_is=True
)
```

```python
sn.sql.cnt_records('sample_table')
```

```python
sn.sql.drop('sample_table')
```
