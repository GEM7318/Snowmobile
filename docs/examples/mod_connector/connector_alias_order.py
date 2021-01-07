"""
Verify credentials order and alias is as laid out as defined in
snowmobile.Connector intro assumptions.
..docs/examples/mod_connector/connector_aliases.py
"""
import snowmobile

sn = snowmobile.Connector()
print(sn.cfg.connection.current)  # > Credentials('creds1')

assert list(sn.cfg.connection.credentials)[:2] == [
    "creds1",
    "creds2",
], "Order of credentials is not as expected"


with open(sn.cfg.location, "r") as r:
    snowmobile_toml_raw = r.read()

assert (
    "default-creds = ''" in snowmobile_toml_raw
), "Value of 'default-creds' has been altered from default"

# --/ freestanding example; should run 'as is' /--
