.. _guides-configuration:

===========================
Configuring the application
===========================

Similar to :mod:`django`, :mod:`cbra` implements a settings module that may
be configured with application-specific settings, and imported from :mod:`cbra.conf`.
The settings module is specified with the :envvar:`PYTHON_SETTINGS_MODULE` environment
variable. It can then be imported from :mod:`cbra.conf`:

.. code-block:: python

    from cbra.conf import settings


To see how this works, enter the following command in a terminal:

.. code-block:: bash

    cd /tmp\
      && echo "EXAMPLE_SETTING='Hello world!'" > settings.py\
      && export PYTHON_SETTINGS_MODULE=settings\
      && python3 -c "from cbra.conf import settings; print(settings.EXAMPLE_SETTING)"

The output from the command above should be ``Hello world!``.

All uppercase symbols in the module specified by :envvar:`PYTHON_SETTINGS_MODULE`
are made avaiable in the settings module, in addition to the environment variables
listed in :ref:`ref-environment-variables`. For duplicate symbols, the order in
which different sources are resolved is as follows:

1. :mod:`cbra` defaults.
2. Environment variables.
3. Default settings from other :mod:`cbra` modules.
4. Module :envvar:`PYTHON_SETTINGS_MODULE`.
5. Deployment environment settings module (see below).
6. :mod:`cbra` constants.

If :envvar:`PYTHON_SETTINGS_MODULE` defines an :attr:`__all__` attribute, then
only symbols listed there are included in the settings module, even if they are
not uppercase.

The :envvar:`DEPLOYMENT_ENV` variable allows the selection of additional settings
based on the environment in which an application is deployed. During initialization
of the :mod:`cbra.conf.settings` module, the :envvar:`PYTHON_SETTINGS_MODULE`
is inspected to have a submodule corresponding to the value of
:envvar:`DEPLOYMENT_ENV`. If such a module is present, then these values are
also imported.


For a list of available settings, see :ref:`ref-available-settings`.
