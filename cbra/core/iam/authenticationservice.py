# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import warnings

from headless.ext.oauth2 import Client

from cbra.types import ICredential
from cbra.types import ICredentialVerifier
from cbra.types import IDependant
from cbra.types import OIDCPrincipal
from cbra.types import RFC9068Principal
from cbra.types import JSONWebToken
from ..ioc.config import TRUSTED_AUTHORIZATION_SERVERS


class AuthenticationService(
    ICredentialVerifier[RFC9068Principal|OIDCPrincipal],
    IDependant
):
    __module__: str = 'cbra.core.iam'
    providers: set[str]

    def __init__(
        self,
        providers: list[str] = TRUSTED_AUTHORIZATION_SERVERS
    ):
        self.providers = set(providers)

    @functools.singledispatchmethod # type: ignore
    async def verify(
        self,
        principal: OIDCPrincipal | RFC9068Principal,
        credential: ICredential | None,
        providers: set[str] | None = None
    ) -> bool:
        if providers: raise NotImplementedError
        warnings.warn(
            f'Unknown principal {type(principal).__name__}. '
            f'{type(self).__name__}.verify(principal, credential) '
            'will always return False.'
        )
        return False

    @verify.register
    async def verify_oidc(
        self,
        principal: OIDCPrincipal,
        credential: JSONWebToken,
        providers: set[str] | None = None
    ) -> bool:
        return await self.verify_oauth_jwt(principal, credential, providers)

    async def verify_oauth_jwt(
        self,
        principal: OIDCPrincipal | RFC9068Principal,
        credential: JSONWebToken,
        providers: set[str] | None = None
    ) -> bool:
        providers = providers or self.providers
        if principal.iss not in providers:
            return False
        async with Client(issuer=principal.iss) as client:
            return await client.verify(str(credential))