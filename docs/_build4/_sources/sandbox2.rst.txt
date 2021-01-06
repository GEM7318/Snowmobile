

:fa:`check, text-success mr-1` Test

========
Sandbox2
========

.. tabbed:: Tab 1

    Tab 1 content

    .. tabbed:: Tab1-sub
       :new-group:

        Tab1-sub content

    .. tabbed:: Tab2-sub

        Tab2-sub content

.. tabbed:: Tab 2

    Tab 2 content

.. tabbed:: Tab 3

    .. code-block:: python

        import pip

.. tabbed:: Tab 4
    :selected:

    .. dropdown:: Nested Dropdown

        Some content




.. tabbed:: From API

    Specify a target directory and export a default **snowmobile.toml** file.

    .. code-block:: python
       :lineno-start: 1

        from pathlib import Path

        from snowmobile import export_config

        export_config(export_dir=Path.cwd())

    The above snippet exports the configuration file to the current working directory.
