.. _ref-available-settings:

==================
Available settings
==================

This document lists the recognized symbol names for use with
:mod:`cbra.conf.settings`.

.. module:: cbra.core.conf.settings


.. attribute:: DEPENDENCIES

  The list of dependencies that are injected during application boot-time. It
  consists of dictionaries describing under what name a dependency must be
  injected and how it should be resolved.

  An example is shown below:

  .. code-block:: python

    # settings.py
    DEPENDENCIES = [
        {
          'name': "ExampleDependency",
          'qualname': 'import.path.to.dependency'
        }
    ]


.. attribute:: TRUSTED_AUTHORIZATION_SERVERS

  The list of trusted OAuth 2.x/OpenID Connect authorization servers.
  The :mod:`cbra.core.iam` framework will reject bearer tokens that
  are not issued by these servers.