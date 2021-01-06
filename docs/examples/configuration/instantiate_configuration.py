"""
Instantiate a snowmobile.Configuration object directly.
../docs/examples/configuration/instantiate_configuration.py
"""

import snowmobile

cfg = snowmobile.Configuration()

type(cfg)  # > snowmobile.core.configuration.Configuration
vars(cfg)
