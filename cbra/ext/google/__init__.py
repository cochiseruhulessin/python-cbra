"""
=====================================================
:mod:`cbra.ext.google` - Google integration framework
=====================================================

The :mod:`cbra.ext.google` provides integration with various
Google Cloud Platform services.

Classes, functions and constants
================================

.. autoclass:: cbra.ext.google.GoogleEndpoint
  :members: allowed_service_accounts

  An implementation of :class:`~cbra.core.Endpoint`. This implementation
  is used to build endpoints that are invoked by Google services, such
  as Eventarc or Cloud Scheduler. Google services authenticate themselves
  with an OpenID Connect ID token, which is verified by this endpoint
  against the Google authorization server at https://accounts.google.com.

  To get an idea of a basic implementation, refer to the Google Eventarc
  implementation:

  .. literalinclude:: ../../../../cbra/ext/google/eventarcendpoint.py
    :language: python
    :lines: 10-


Environment variables
=====================

:mod:`cbra.ext.google` supports two types of environment variables:

* `Default environment variables`_
* `User-defined environment variables`_

Both are merged together during application boot.

Default environment variables
-----------------------------
No default environment variables are yet specified.

User-defined environment variables
----------------------------------
The following user-defined environment variables are supported.

.. envvar:: GOOGLE_SERVICE_ACCOUNT_EMAIL

  If the application is deployed in a Compute Engine or Cloud
  Run instance, this environment indicates the attached service
  account that represents the services' identity. It is also
  automatically accepted as a principal when invoking
  :class:`~cbra.ext.google.GoogleEndpoint` and its subclasses.
"""
# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .eventarcendpoint import EventarcEndpoint
from .googleendpoint import GoogleEndpoint
from .googlepubsubtransport import GooglePubsubTransport
from .googleserviceaccountprincipal import GoogleServiceAccountPrincipal
from .service import Service


__all__: list[str] = [
    'EventarcEndpoint',
    'GoogleEndpoint',
    'GooglePubsubTransport',
    'GoogleServiceAccountPrincipal',
    'Service'
]