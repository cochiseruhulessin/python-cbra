.. _ref-environment-variables:

=====================
Environment variables
=====================

This document lists the environment variables recognized by the
:mod:`cbra` framework. Environment variables listed in this
document are also made available through :mod:`cbra.conf.settings`.


.. envvar:: DEBUG

-----------------

Enable debug mode by setting this enviroment variable to ``1``.


.. envvar:: DEPLOYMENT_ENV

--------------------------

The current deployment environment. This may be any value, but the
following values have predefined meanings:

- ``production`` - A production environment.
- ``local`` - A local development environment. This may enable certain
  debug features. **No instance running in a public environment should
  run with this value.**

.. warning::

  :envvar:`DEPLOYMENT_ENV` is a sensitive environment variable and
  must only be set by trusted sources. Allowing untrusted parties to
  specify the :envvar:`DEPLOYMENT_ENV` variable, may lead to
  denial-of-service, degraded performance or remote code execution.

The value must consist of alphanumeric characters only, and must not
start with a number.


.. envvar:: HTTP_WORKER_TIMEOUT

-------------------------------

Timeout in seconds for HTTP workers. Defaults to ``180``.


.. envvar:: LOCALHOST_SSL_CRT

-----------------------------

The filepath to an X.509 certificate that  is used with TLS connections in
local development servers.

The certificate must contain the following Subject Alternative Names (SANs),
as defined in :rfc:`2606`:

- ``localhost``
- ``*.localhost``
- ``*.example``
- ``*.invalid``
- ``*.test``

Additional subdomains may be listed for specific use cases, but the certificate
MUST NOT include any non-reserved TLD.

This certificate is assumed to be trusted by the operating system.

If :envvar:`LOCALHOST_SSL_CRT` is not defined or the file specified does not
exist, then default to ``pki/server/noop.crt``. If that file also does not
exist, :envvar:`LOCALHOST_SSL_CRT` will be ``None``.


.. envvar:: LOCALHOST_SSL_KEY

-----------------------------

The filepath to private key that is used with TLS connections in local
development servers.

If :envvar:`LOCALHOST_SSL_KEY` is not defined or the file specified does not
exist, then default to ``pki/server/noop.key``. If that file also does not
exist, :envvar:`LOCALHOST_SSL_KEY` will be ``None``.


.. envvar:: PYTHON_SETTINGS_MODULE

----------------------------------

Points to the settings module used by an application. This value is mandatory
when using :mod:`cbra.conf.setttings`.


.. envvar:: WEB_CONCURRENCY

---------------------------

Specifies the number of workers that may be spawned in the context
of an HTTP web server.
