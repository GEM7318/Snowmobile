
# imports
import pandas as pd
import numpy as np
np.random.seed(1)


# some dummy data
df = pd.DataFrame(
	data={
		"id_col": [v for v in range(1, 11)],
		"metric1": np.random.randint(low=1, high=100, size=10),
		"metric2": np.random.normal(0.0, 1.0, size=10),
		"metric3": np.random.normal(0.0, 1.0, size=10),
	}
)

from pathlib import Path

Path.cwd() / 'docs' / 'usage_crash_course' / 'sample.html'

import snowmobile

sn: snowmobile.Connector = snowmobile.Connect(creds='sandbox')


