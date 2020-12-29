# snowmobile

## Resources
- Description


- Quick Start
    - Installation
    - Basic Usage

    
- `snowmobile.toml`
    - Description / validation
    - Caching
    - Minimum configuration
    - Structure
      - Connection
        - Credentials
        - Default-settings
      - Loading
        - file-format
        - if-exists-behavior
        - put, copy
        - export-options
      - External files
      - Query
      - Script
        - export-dir-name
        - patterns
        - qa
        - markdown
    
    
- `snowmobile` API
    - connector
        - arguments
            - delay
            - creds
            - config_file_nm
            - from_config
        - attributes
            - snowflake.connector
            - cfg
            - sql
        - methods
            - connect/disconnect/query/ex
    - loader
    - statement
      - extended classes
    - script
      - statements
      - markup

    
- [README](README.md)
- [Core-API Reference](Core-API%20Reference.md)
- [Authors](authors.md)
- [License](license.md)
- [Changelog](changelog.md)
- [Creds](creds.md)

## Other
- [Module-Index](modindex.md)
- [Index](genindex.md)




this file is parsed into a `snowmobile.Configuration` object using [pydantic's](https://pydantic-docs.helpmanual.io/) every piece the parsing and validation of `snowmobile` objects from this file is done each component of this file is its own  

- Aliasing multiple credentials and connection options for easy access through the same Python API
- Specifying global connection options, credentials-specific over-rides, or over-riding both with keyword arguments passed directly to the API



 host of objects built to enable management of of configuration management options to make streamline their usage. It's designed to store credentials, connection settings, and data loading specifications in a single **snowmobile.toml** file which can be read from any virtual
environment or project on a given machine.

Its core functionality includes:

- Providing easy access to `snowflake.connector` and `snowflake.cursor` objects
- Maintain a single Snowflake configuration file for all projects on a given machine, including:
  - Caching the location of this file across projects and re-locating if its location changes
  - Optionally provide a full path to a specific configuration file if preferable for container-based solutions
- Store, alias, and access multiple sets of credentials through the same Python API
- Specify global connection settings w/ options to over-ride at the *credentials* level or through keyword arguments passed directly to the API






`snowmobile` caches its location so that users have access to  to consistent functionality across projects and environments without , which is able to be accessed by
other projects or environments on a given machine; `snowmobile` caches its location and the first time this file is found, `snowmobile` keeps track of the location of this file 

will locate the first time a `snowmobile` will cache its
location From this, `snowmobile`'s object
model is instantiated which in which credentials, connection arguments,
and other configurations are stored that all projects and environments have access to.


intended to be unique for a given operating system or container which is then cached   

Its design is focused on enabling:

- The use a single configuration file for credentials and other configuration options for all projects running on a given machine
- Parsing 

