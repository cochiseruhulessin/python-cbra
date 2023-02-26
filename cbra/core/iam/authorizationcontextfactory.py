# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any
from typing import Awaitable

import fastapi

from cbra.core.conf import settings
from cbra.types import Forbidden
from cbra.types import IAuthorizationContextFactory
from cbra.types import IDependant
from cbra.types import IRequestPrincipal
from cbra.types import ISubjectResolver
from cbra.types import UnauthenticatedAuthorizationContext
from ..ioc import instance
from ..utils import ensure_awaited
from .authenticatedcontext import AuthenticatedContext
from .authenticationservice import AuthenticationService
from .subject import Subject
from .subjectresolver import SubjectResolver


class AuthorizationContextFactory(IAuthorizationContextFactory, IDependant):
    """The default implementation of :class:`~cbra.types.IAuthorizationContextFactory`"""
    __module__: str = 'cbra.core.iam'
    authentication: AuthenticationService
    logger: logging.Logger = logging.getLogger('uvicorn')
    resolver: ISubjectResolver

    def __init__(
        self,
        resolver: ISubjectResolver = instance(
            name='SubjectResolver',
            missing=SubjectResolver
        ),
        authentication: AuthenticationService = instance(
            name='AuthenticationService',
            missing=AuthenticationService
        )
    ):
        self.authentication = authentication
        self.resolver = resolver

    def allowed_audience(self, request: fastapi.Request) -> set[str]:
        url = request.url
        allow = {
            f'{url.scheme}://{url.netloc}',
            str(url)
        }

        # If the ASGI_ROOT_PATH setting is defined, then we have a problem
        # with Eventarc and Cloud Scheduler, which use the URL without
        # the prefix. For now the solution is to also allow a URL with
        # the ASGI_ROOT_PATH stripped from the path, but its quite a
        # hack and must be fixed (TODO). Also we must validate that
        # the path starts with a slash somewhere else.
        if settings.ASGI_ROOT_PATH:
            if not str.startswith(settings.ASGI_ROOT_PATH, '/'):
                raise ValueError('ASGI_ROOT_PATH must begin with a slash.')
            if str.endswith(settings.ASGI_ROOT_PATH, '/'):
                raise ValueError('ASGI_ROOT_PATH must not end with a slash.')
            path = str.lstrip(url.path, settings.ASGI_ROOT_PATH)
            if not str.startswith(path, '/'):
                path = f'/{path}'
            allow.add(f'{url.scheme}://{url.netloc}{path}')
        return allow

    async def authenticate(
        self,
        request: fastapi.Request,
        principal: IRequestPrincipal,
        providers: set[str] | None = None,
        subjects: set[str] | Awaitable[set[str]] | None  = None,
        claims: dict[str, Any] | None = None
    ):
        remote_host = request.client.host if request.client else None
        subject = await principal.resolve(self.resolver.resolve)
        await subject.authenticate(
            self.authentication,
            providers=providers
        )
        if principal.has_audience():
            self.validate_audience(principal, self.allowed_audience(request))

        unauthenticated= UnauthenticatedAuthorizationContext(remote_host=remote_host)
        if not subject.is_authenticated():
            return unauthenticated

        # Determine if the subject is in the allowed subjects list.
        subjects = await ensure_awaited(subjects) or set()
        if subjects and subject.sub not in subjects:
            self.logger.critical(
                'Subject %s is not in the allowed subjects list',
                subject.sub
            )
            return unauthenticated

        return AuthenticatedContext(
            remote_host=remote_host,
            subject=subject
        )

    def _is_authenticated(
        self,
        request: fastapi.Request,
        subject: Subject,
        principal: IRequestPrincipal
    ) -> bool:
        return all([
            subject.is_authenticated(),
            self.is_authenticated(request, subject, principal)
        ])

    def is_authenticated(
        self,
        request: fastapi.Request,
        subject: Subject,
        principal: IRequestPrincipal
    ) -> bool:
        """Hook to determine if the request is succesfully authenticated.
        The default implementation always returns ``True``, but may be
        overriden to implement additional authenticated logic.
        """
        return True

    def validate_audience(self, principal: IRequestPrincipal, allow: set[str]):
        if not principal.validate_audience(allow):
            self.logger.critical(
                'Received a principal/credential combination with an '
                'audience that is not accepted by the server (allowed'
                ': %s, actual: %s)',
                str.join(', ', allow),
                str.join(', ', principal.get_audience()),
            )
            raise Forbidden