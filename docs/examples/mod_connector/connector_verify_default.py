"""
Verify `default-creds` has been changed to `creds2`.
../examples/mod_connector/connector_verify_default.py
"""
import snowmobile

sn = snowmobile.Connector()

assert sn.cfg.connection.default_alias == 'creds2', (
    "Something's not right here; expected default_alias =='creds2'"
)

# --/ freestanding example; should run 'as is' /--
