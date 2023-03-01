# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
""".. _ref-available-settings:

==================
Available settings
==================

This document lists the recognized symbol names for use with
:mod:`cbra.conf.settings`.

.. module:: cbra.core.conf.settings


.. setting:: ASGI_ROOT_PATH

``ASGI_ROOT_PATH``
==================

Default: ``None``

The root path of the application. Use this setting when running behind
a proxy and the application is served from something else than ``/``
e.g. ``/api/v1``.

.. setting:: DEBUG

``DEBUG``
---------

Default: ``False``

A boolean that turns on/off debug mode.

Never deploy an application into production with :setting:`DEBUG` turned on.


.. setting:: DEPENDENCIES

``DEPENDENCIES``
================

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


.. setting: DEPLOYMENT_ENV

``DEPLOYMENT_ENV``
==================

Default: ``'production'``

The current deployment environment. This defaults to the string
``production`` in order to prevent applications being deployed
with less secure settings from other environments.


.. setting:: LOG_CONSOLE

``LOG_CONSOLE``
---------------

Default: ``False``

Enable logging to ``stdout``.


.. setting: OAUTH2_CLIENTS

``OAUTH2_CLIENTS``
==================
The list of OAuth 2.x/OpenID Connect clients that are used by the
application. Example:

.. code:: python

    OAUTH2_CLIENTS = [
        {
            'issuer: 'https://accounts.google.com',
            'client_id': 'myclient',
            'client_secret': 'mysecret'
        }
    ]


.. setting: OAUTH2_ISSUER

``OAUTH2_ISSUER``
=================

  Default: ``None``

  The issuer identifier used by this server.


.. setting: SECRET_KEY

``SECRET_KEY``
==============

Default: ``''`` (Empty string)

A secret key for a particular CBRA application. This is used to provide
cryptographic signing, and should be set to either:

* a string holding a unique, unpredictable value.
* a reference to a key.

This value may also be provided as an environment variable.

**Note that this key should not be used for long-term storage.
It may be rotated without the knowledge of the application, so
any code that uses this setting must gracefully handle verification
and/or decryption failures.**

.. warning::

    **Keep this value secret.**

    Running CBRA with a known :setting:`SECRET_KEY` defeats many of CBRA's
    security protections, and can lead to privilege escalation and remote code
    execution vulnerabilities


.. setting:: SESSION_COOKIE_AGE

``SESSION_COOKIE_AGE``
======================

Default: ``1209600`` (2 weeks, in seconds)

The age of session cookies, in seconds.


.. setting:: SESSION_COOKIE_DOMAIN

``SESSION_COOKIE_DOMAIN``
=========================

Default: ``None``

The domain to use for session cookies. Set this to a string such as
``"example.com"`` for cross-domain cookies, or use ``None`` for a standard
domain cookie.

Be cautious when updating this setting on a production site. If you update
this setting to enable cross-domain cookies on a site that previously used
standard domain cookies, existing user cookies will be set to the old
domain. This may result in them being unable to log in as long as these cookies
persist.


.. setting:: SESSION_COOKIE_HTTPONLY

``SESSION_COOKIE_HTTPONLY``
===========================

Default: ``True``

Whether to use ``HttpOnly`` flag on the session cookie. If this is set to
``True``, client-side JavaScript will not be able to access the session
cookie.

HttpOnly_ is a flag included in a Set-Cookie HTTP response header. It's part of
the :rfc:`6265#section-4.1.2.6` standard for cookies and can be a useful way to
mitigate the risk of a client-side script accessing the protected cookie data.

This makes it less trivial for an attacker to escalate a cross-site scripting
vulnerability into full hijacking of a user's session. There aren't many good
reasons for turning this off. Your code shouldn't read session cookies from
JavaScript.

.. _HttpOnly: https://owasp.org/www-community/HttpOnly


.. setting:: SESSION_COOKIE_NAME

``SESSION_COOKIE_NAME``
=======================

Default: ``'session'``

The name of the cookie to use for sessions. This can be whatever you want
(as long as it's different from the other cookie names in your application).


.. setting:: SESSION_COOKIE_PATH

``SESSION_COOKIE_PATH``
=======================

Default: ``'/'``

The path set on the session cookie. This should either match the URL path of your
installation or be parent of that path.

This is useful if you have multiple instances running under the same
hostname. They can use different cookie paths, and each instance will only see
its own session cookie.


.. setting:: SESSION_COOKIE_SAMESITE

``SESSION_COOKIE_SAMESITE``
===========================

Default: ``'Lax'``

The value of the `SameSite`_ flag on the session cookie. This flag prevents the
cookie from being sent in cross-site requests thus preventing CSRF attacks and
making some methods of stealing session cookie impossible.

Possible values for the setting are:

* ``'Strict'``: prevents the cookie from being sent by the browser to the
  target site in all cross-site browsing context, even when following a regular
  link.

  For example, for a GitHub-like website this would mean that if a logged-in
  user follows a link to a private GitHub project posted on a corporate
  discussion forum or email, GitHub will not receive the session cookie and the
  user won't be able to access the project. A bank website, however, most
  likely doesn't want to allow any transactional pages to be linked from
  external sites so the ``'Strict'`` flag would be appropriate.

* ``'Lax'`` (default): provides a balance between security and usability for
  websites that want to maintain user's logged-in session after the user
  arrives from an external link.

  In the GitHub scenario, the session cookie would be allowed when following a
  regular link from an external website and be blocked in CSRF-prone request
  methods (e.g. ``POST``).

* ``'None'`` (string): the session cookie will be sent with all same-site and
  cross-site requests.

* ``False``: disables the flag.

.. _SameSite: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite


.. setting:: SESSION_COOKIE_SECURE

``SESSION_COOKIE_SECURE``
=========================

Default: ``True``

Whether to use a secure cookie for the session cookie. If this is set to
``True``, the cookie will be marked as "secure", which means browsers may
ensure that the cookie is only sent under an HTTPS connection.

Leaving this setting off isn't a good idea because an attacker could capture an
unencrypted session cookie with a packet sniffer and use the cookie to hijack
the user's session.


.. setting:: TRUSTED_AUTHORIZATION_SERVERS

``TRUSTED_AUTHORIZATION_SERVERS``
=================================
The list of trusted OAuth 2.x/OpenID Connect authorization servers.
The :mod:`cbra.core.iam` framework will reject bearer tokens that
are not issued by these servers.
"""
import importlib
import types
import os
from typing import cast
from typing import Any


class Settings:
    user: types.ModuleType | None = None
    ASGI_ROOT_PATH: str | None
    DEPLOYMENT_ENV: str
    DEBUG: bool
    LOGIN_AUTHORIZED_DOMAINS: set[str]
    LOG_CONSOLE: bool
    LOGGING: dict[str, Any]
    OAUTH2_CLIENTS: list[Any]
    OAUTH2_ISSUER: str
    SECRET_KEY: str
    SESSION_COOKIE_AGE: int
    SESSION_COOKIE_DOMAIN: str | None
    SESSION_COOKIE_HTTPONLY: bool
    SESSION_COOKIE_NAME: str
    SESSION_COOKIE_PATH: str
    SESSION_COOKIE_SAMESITE: bool | str | None
    SESSION_COOKIE_SECURE: bool
    TRUSTED_AUTHORIZATION_SERVERS: list[str]

    __defaults__: dict[str, Any] = {
        'ASGI_ROOT_PATH': os.environ.get('ASGI_ROOT_PATH'),
        'DEBUG': False,
        'DEPLOYMENT_ENV': os.environ.get('DEPLOYMENT_ENV') or 'production',
        'LOGIN_AUTHORIZED_DOMAINS': set(),
        'LOG_CONSOLE': False,
        'LOGGING': {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                "uvicorn": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(message)s",
                    "use_colors": None,
                },
                "stdout": {
                    "fmt": "%(message)s",
                },
            },
            'handlers': {
                'default': {
                    'formatter': "uvicorn",
                    'class': "logging.StreamHandler",
                    'stream': "ext://sys.stdout",
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': "ext://sys.stdout",
                    'formatter': 'uvicorn'
                }
            },
            'loggers': {
                'aorta': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': 'INFO'
                },
                'cbra': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': 'INFO'
                }
            }
        },
        'OAUTH2_CLIENTS': [],
        'OAUTH2_ISSUER': None,
        'SECRET_KEY': os.environ.get('SECRET_KEY') or bytes.hex(os.urandom(32)),
        'SESSION_COOKIE_AGE': 1209600,
        'SESSION_COOKIE_DOMAIN': None,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_NAME': 'session',
        'SESSION_COOKIE_PATH': '/',
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SESSION_COOKIE_SECURE': True,
        'TRUSTED_AUTHORIZATION_SERVERS': []
    }

    def register(self, name: str, default: Any = NotImplemented):
        if name in self.__defaults__:
            raise ValueError(f'Setting already registered: {name}')
        if str.upper(name) != name:
            raise ValueError(f'Settings must be uppercase.')
        if default != NotImplemented:
            self.__defaults__[name] = default

    def __getattr__(self, __name: str) -> Any:
        try:
            self.user = importlib.import_module(os.environ['PYTHON_SETTINGS_MODULE'])
        except (ImportError, KeyError):
            self.user = None
        if str.upper(__name) != __name:
            raise AttributeError(f'No such setting: {__name}')
        try:
            return getattr(self.user, __name)
        except AttributeError:
            if __name not in self.__defaults__:
                raise AttributeError(f'No such setting: {__name}')
            return self.__defaults__[__name]


settings: Settings = cast(Any, Settings()) # type: ignore