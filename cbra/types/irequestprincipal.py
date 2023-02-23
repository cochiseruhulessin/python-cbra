# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi

from .icredential import ICredential
from .irequestprincipalintrospecter import IRequestPrincipalIntrospecter
from .isubject import ISubject


P = TypeVar('P', bound='IRequestPrincipal')


class IRequestPrincipal:
    __module__: str = 'cbra.types'

    @classmethod
    def depends(cls: type[P]) -> P:
        return fastapi.Depends(cls.fromrequest)

    @classmethod
    async def fromrequest(cls: type[P], request: fastapi.Request) -> P:
        """Create a new principal from the request object."""
        return cls.parse_obj({ # type: ignore
            'request': request,
            'headers': request.headers,
            'cookies': request.cookies,
            'content': (
                await request.body()
                if 'Content-Type' in request.headers
                else None
            )
        })

    def get_audience(self) -> set[str]:
        """Return the audience(s) of the principal."""
        raise NotImplementedError

    def get_credential(self) -> ICredential | None:
        """Return the credential from which the principal was instantiated."""
        raise NotImplementedError

    def has_audience(self) -> bool:
        """Return a boolean indicating if the principal targets a specific
        audience.
        """
        raise NotImplementedError

    def is_anonymous(self) -> bool:
        """Return a boolean indicating if the principal was anonymous
        i.e. did not provide identifying information or credentials
        at all.
        """
        raise NotImplementedError

    def must_introspect(self) -> bool:
        """Return a boolean indicating if the principal must be
        introspected to obtain information about the subject.
        """
        return False

    def validate_audience(self, allow: set[str]) -> bool:
        """Return a boolean indicating if the principal targets
        *any* of the given audiences.
        """
        raise NotImplementedError

    async def resolve(
        self: P,
        resolve: Callable[[P], Awaitable[ISubject]]
    ) -> ISubject:
        return await resolve(self)

    async def introspect(
        self: P,
        introspecter: IRequestPrincipalIntrospecter
    ) -> P:
        """Introspect an opaque principal such as a generic bearer token
        or a session identifier.
        """
        return await introspecter.introspect(self)

    async def verify(
        self: P,
        verify: Callable[[P, ICredential | None], Awaitable[bool]]
    ) -> bool:
        return await verify(self, self.get_credential())

    