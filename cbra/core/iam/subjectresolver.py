# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import warnings

from cbra.types import IRequestPrincipal
from cbra.types import ISubject
from cbra.types import ISubjectResolver
from cbra.types import NullRequestPrincipal
from cbra.types import NullSubject
from cbra.types import OIDCRequestPrincipal
from cbra.types import RFC9068RequestPrincipal
from cbra.types import SessionRequestPrincipal
from .subject import Subject


class SubjectResolver(ISubjectResolver):
    __module__: str = 'cbra.core.iam'

    @functools.singledispatchmethod # type: ignore
    async def resolve(self, principal: IRequestPrincipal) -> ISubject:
        warnings.warn(
            f'{type(self).__name__} does not know how to resolve '
            f'{type(principal).__name__}, returning NullSubject.'
        )
        return NullSubject()

    @resolve.register
    async def resolve_null(
        self,
        principal: NullRequestPrincipal
    ) -> ISubject:
        return NullSubject()

    @resolve.register
    async def _resolve_oidc(
        self,
        principal: OIDCRequestPrincipal
    ) -> ISubject:
        return await self.resolve_oidc(principal)

    async def resolve_oidc(
        self,
        principal: OIDCRequestPrincipal
    ) -> ISubject:
        return Subject(
            email=principal.email,
            id=principal.sub,
            principal=principal
        )

    @resolve.register
    async def _resolve_rfc9068(
        self,
        principal: RFC9068RequestPrincipal
    ) -> ISubject:
        return await self.resolve_rfc9068(principal)

    async def resolve_rfc9068(
        self,
        principal: RFC9068RequestPrincipal
    ) -> ISubject:
        return Subject(
            email=None,
            id=principal.sub,
            principal=principal
        )

    @resolve.register
    async def _resolve_session(
        self,
        principal: SessionRequestPrincipal
    ) -> ISubject:
        return await self.resolve_session(principal)

    async def resolve_session(
        self,
        principal: SessionRequestPrincipal
    ) -> ISubject:
        assert principal.claims is not None
        assert principal.claims.sub is not None
        return Subject(
            id=principal.claims.sub,
            email=principal.claims.email,
            principal=principal
        )