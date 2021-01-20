"""
Instantiate a snowmobile.Configuration object directly.
../docs/snippets/instantiate_configuration.py
"""

import snowmobile

cfg = snowmobile.Configuration()

type(cfg)  # > snowmobile.core.configuration.Configuration
vars(cfg)
