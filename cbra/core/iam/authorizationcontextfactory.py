# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import IAuthorizationContextFactory
from cbra.types import IDependant
from cbra.types import IPrincipal
from cbra.types import ISubjectResolver
from cbra.types import UnauthenticatedAuthorizationContext
from ..ioc import instance
from .authenticatedcontext import AuthenticatedContext
from .authenticationservice import AuthenticationService
from .subject import Subject
from .subjectresolver import SubjectResolver


class AuthorizationContextFactory(IAuthorizationContextFactory, IDependant):
    """The default implementation of :class:`~cbra.types.IAuthorizationContextFactory`"""
    __module__: str = 'cbra.core.iam'
    authentication: AuthenticationService
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

    async def authenticate(
        self,
        request: fastapi.Request,
        principal: IPrincipal
    ):
        remote_host = request.client.host if request.client else None
        subject = await principal.resolve(self.resolver.resolve)
        await subject.authenticate(self.authentication)
        if not subject.is_authenticated():
            return UnauthenticatedAuthorizationContext(remote_host=remote_host)
        return AuthenticatedContext(
            remote_host=remote_host,
            subject=subject
        )

    def _is_authenticated(
        self,
        request: fastapi.Request,
        subject: Subject,
        principal: IPrincipal
    ) -> bool:
        return all([
            subject.is_authenticated(),
            self.is_authenticated(request, subject, principal)
        ])

    def is_authenticated(
        self,
        request: fastapi.Request,
        subject: Subject,
        principal: IPrincipal
    ) -> bool:
        """Hook to determine if the request is succesfully authenticated.
        The default implementation always returns ``True``, but may be
        overriden to implement additional authenticated logic.
        """
        return True