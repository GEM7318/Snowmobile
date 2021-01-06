

.. tabbed:: Quick Start

   **1. Installation**

   ``pip install snowmobile``

   **2. Export snowmobile.toml**

   .. code-block:: python

      import snowmobile
      from pathlib import Path

      snowmobile.Configuration(export_dir=Path.cwd())

   Provide a target directory to the **export_dir** argument of `snowmobile.Configuration`
   to export a default *snowmobile.toml* file; the above snippet exports to the current
   working directory.


   **3. Store Credentials**

   .. literalinclude:: ../snowmobile/core/pkg_data/snowmobile_TEMPLATE.toml
     :language: toml
     :lineno-start: 2
     :lines: 2-26
     :emphasize-lines: 4, 22

   .. note:

      All that's required for minimum configuration is:
        1. **Specify a valid set of credentials within the ``[connection.credentials.creds1]`` block**
        2. **Modify or remove any unwanted arguments within the ``[connection.default-arguments]`` block**

   **4. import snowmobile**

   .. literalinclude:: ./examples/setup/quick_intro_connector.py
     :language: python
     :lineno-start: 1
     :lines: 5-7

   With the expected console output ending with something like:
    >>>
    Looking for snowmobile.toml in local file system..
    (1 of 1) Located 'snowmobile.toml' at ../Snowmobile/snowmobile.toml
    ..connected: snowmobile.Connect(creds='creds1')

.. tabbed:: Crash Course

   .. code-block:: python

      import snowmobile

      sn = snowmobile.Connect()
