# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
""".. _guides-authentication:

=======================
Authenticating requests
=======================
The :mod:`cbra` module comes with a basic authentication system that enables
resolving an incoming HTTP request to a subject identifier, based on the
parameters included in the request, such as headers or cookies. A subject
identifier uniquely points to an account of some kind (user account, service
account) that has access to certain protected resources.

What is authentication?
=======================
Authentication is a term that refers to the process of proving that some fact
or some document is genuine. In computer science, this term is typically
associated with proving a user's identity. The process of authentication can
thus be modelled into three models:

- A **Subject** is a person or a service that has one or many identities.
- A **Principal** represents a specific identity of a Subject, such as
  an email address, phone number or account identifier.
- A **Credential** is used to assert the ownership of or access to a
  specific Principal.

Practically speaking, *authentication* may then be defined as follows:

A **Subject** uses a combination of a **Principal** and a **Credential** to
assert its identity. These concepts are reflected in the abstract interfaces
specified by :mod:`cbra.types`, being :class:`~cbra.types.ICredential`,
:class:`~cbra.types.IRequestPrincipal` and :class:`~cbra.types.ISubject`. The default
implementation in :mod:`cbra.core.iam` supports RFC 9068 and
OpenID Connect ID Tokens to authenticate requests, but can quite easily
extended to support other mechanisms, like your own bearer token.


Configuring authentication
==========================
Configuring :mod:`cbra` with the default implementation is as simple as setting
:attr:`~cbra.core.conf.settings.TRUSTED_AUTHORIZATION_SERVERS` in your settings
module:

.. code:: python

    # settings.py
    TRUSTED_AUTHORIZATION_SERVERS: list[str] = [
        'https://accounts.google.com'
    ]


Authenticated requests
======================
The :mod:`cbra` IAM framework may be used with :class:`~cbra.core.Endpoint`
and :class:`cbra.core.Resource`, or plain functions as you might be used to
with FastAPI:

.. code:: python

    import fastapi
    import cbra.core as cbra
    from cbra.core.iam import AuthorizationContextFactory
    from cbra.types import Principal

    app: cbra.Application = cbra.Application()

    @app.get('/')
    async def f(
        request: fastapi.Request,
        factory: AuthorizationContextFactory = fastapi.Depends(),
        principal: Principal = fastapi.Depends(Principal.fromrequest)
    ):
        ctx = await factory.authenticate(request, principal)
        return {
            'remote_host': ctx.remote_host,
            'is_authenticated': ctx.is_authenticated()
        }

    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app)

Similarly, :class:`~cbra.core.Endpoint` and :class:`~cbra.core.Resource`
may be used with the authentication framework:

.. code:: python

    import cbra.core as cbra


    class AuthenticatedEndpoint(cbra.Endpoint):

        async def get(self) -> dict[str, bool | str]:
            return {
                'remote_host': str(self.ctx.remote_host),
                'is_authenticated': self.ctx.is_authenticated()
            }


    app: cbra.Application = cbra.Application()
    app.inject('TRUSTED_AUTHORIZATION_SERVERS', ['https://accounts.google.com'])
    app.add(AuthenticatedEndpoint)


    if __name__ == '__main__':
        import uvicorn
        uvicorn.run('__main__:app', reload=True)

To run the above example, the following script obtains an OpenID Connect
ID Token from Google:

.. code:: python

    import google.oauth2.id_token
    import google.auth.transport.requests

    if __name__ == '__main__':
        request = google.auth.transport.requests.Request()
        audience = 'http://localhost:8000'
        id_token = google.oauth2.id_token.fetch_id_token(request, audience)
        headers = {'Authorization': f'bearer {id_token}'}
        print(id_token)
"""
from .authenticatedcontext import AuthenticatedContext
from .authenticationservice import AuthenticationService
from .authorizationcontextfactory import AuthorizationContextFactory
from .isubjectrepository import ISubjectRepository
from .subject import Subject as RequestSubject
from .subjectresolver import SubjectResolver
from .types import IUserOnboardingService


__all__: list[str] = [
    'AuthenticatedContext',
    'AuthenticationService',
    'AuthorizationContextFactory',
    'ISubjectRepository',
    'IUserOnboardingService',
    'RequestSubject',
    'SubjectResolver',
]