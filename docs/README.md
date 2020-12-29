# snowmobile

[![Documentation Status](https://readthedocs.org/projects/snowmobile/badge/?version=latest)](https://snowmobile.readthedocs.io/en/latest/?badge=latest#)
[![codecov](https://codecov.io/gh/GEM7318/Snowmobile/branch/0.2.1/graph/badge.svg?token=UCMCWRIIJ8)](https://codecov.io/gh/GEM7318/Snowmobile)
[![PyPI version](https://badge.fury.io/py/snowmobile.svg)](https://badge.fury.io/py/snowmobile)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/GEM7318/Snowmobile/blob/master/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`snowmobile` is a thick wrapper around the [Snowflake Connector for Python](https://docs.snowflake.com/en/user-guide/python-connector.html) that bundles the existing Snowflake `Connection` and `Cursor` into an object model focused on configuration management and streamlining interacting with the database through Python.

At its core, `snowmobile` provides a single configuration file, *snowmobile.toml*, which can be accessed by any number of Python instances on a given machine. Internally, each component of this file is its own [pydantic](https://pydantic-docs.helpmanual.io/) object, which performs type validation of all fields upon each instantiation; these specifications include **credentials**, **connection options**, **script execution specifications**, **file formats**, **mapping to local DDL and more**, including support for aliases such that different sets of credentials, connection arguments, and data loading specifications can be accessed through the same Python API.
