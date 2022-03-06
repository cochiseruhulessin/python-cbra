.. _ref-available-settings:

==================
Available settings
==================

This document lists the recognized symbol names for use with
:mod:`cbra.conf.settings`.

.. module:: cbra.conf.settings


.. attribute:: DEPENDENCIES

  The list of dependencies that are injected during application boot-time. It
  consists of dictionaries describing under what name a dependency must be
  injected and how it should be resolved. Each dictionary must have a ``type``
  member indicating the source from which the dependency is resolved, and a
  ``name`` member specifying under which name the dependency is found. Valid
  types are:

  - ``file`` - Loads a file from the local filesystem. The parameters are:

    .. code-block:: python

        {
            'type': "file",
            'name': "ExampleDependency",
            'path': "relative/or/absolute/path"
        }

  - ``symbol`` - Imports the specified symbol and makes it available under the
    given ``name``:

    .. code-block:: python

        {
            'type': "symbol",
            'name': "ExampleDependency",
            'value': "qualname.to.python.symbol"
        }

  An example is shown below:

  .. code-block:: python

    # settings.py
    DEPENDENCIES = [
        {
          'type': 'symbol',
          'name': "ExampleDependency",
          'value': "__main__.EXAMPLE_DEPENDENCY"
        }
    ]

  .. literalinclude:: ../../../examples/run-dependant.py
