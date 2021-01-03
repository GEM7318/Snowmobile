

**1. Installation**

``pip install snowmobile``

**2. Export snowmobile.toml**

.. tabbed:: From API

    Specify a target directory and export a default **snowmobile.toml** file.

    .. code-block:: python
       :lineno-start: 1

        from pathlib import Path

        from snowmobile import export_config

        export_config(export_dir=Path.cwd())

    The above snippet exports the configuration file to the current working directory.

.. tabbed:: Copy File Contents

    Copy the contents below in a file called **snowmobile.toml** anywhere on your local file
    system.

    .. literalinclude:: ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
        :language: toml
        :lineno-start: 1

**3. Store A Set Credentials**

The first few lines of **snowmobile.toml** are outlined below; **for minimum configuration**:
       1. Specify a valid set of credentials within the **[connection.credentials.creds1]** block
       2. Modify or remove any unwanted arguments within the **[connection.default-arguments]** block

.. literalinclude:: ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
   :language: toml
   :lineno-start: 2
   :lines: 2-26
   :emphasize-lines: 4, 13, 22

.. Tip::
       For initial setup and to ensure replicability of code samples, it's a good idea to:
              1.     Leave *default-creds* as is
              2.     Leave the **aliases** for *creds1* and *creds2* as *creds1* and *creds2*
              3.     Store a second set of credentials under *creds2* if available; if not, store the same set as used
                     for *creds1* under the alias *creds2* as well


**4.** ``import snowmobile`` **and verify connection**

.. literalinclude:: ./examples/setup/quick_intro_connector.py
 :language: python
 :lineno-start: 1
 :lines: 5-7

Successful setup and connection results in ending console output similar to:
    >>>
    Looking for snowmobile.toml in local file system..
    (1 of 1) Located 'snowmobile.toml' at ../Snowmobile/snowmobile.toml
    ..connected: snowmobile.Connect(creds='creds1')
