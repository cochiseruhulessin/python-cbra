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


.. setting: SECRET_KEY

``SECRET_KEY``
==============

Default: ``''`` (Empty string)

A secret key for a particular CBRA application. This is used to provide
cryptographic signing, and should be set to either:

* a string holding a unique, unpredictable value.
* a reference to a key.

.. warning::

    **Keep this value secret.**

    Running CBRA with a known :setting:`SECRET_KEY` defeats many of CBRA's
    security protections, and can lead to privilege escalation and remote code
    execution vulnerabilities


.. setting:: TRUSTED_AUTHORIZATION_SERVERS

``TRUSTED_AUTHORIZATION_SERVERS``
=================================
The list of trusted OAuth 2.x/OpenID Connect authorization servers.
The :mod:`cbra.core.iam` framework will reject bearer tokens that
are not issued by these servers.
"""
from typing import cast
from typing import Any

from unimatrix.conf import settings # type: ignore


settings: Any = cast(Any, settings)