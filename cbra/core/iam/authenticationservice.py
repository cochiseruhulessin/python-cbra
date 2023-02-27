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
from typing import Any

from headless.ext.oauth2 import Client

from cbra.types import HMACSignature
from cbra.types import ICredential
from cbra.types import ICredentialVerifier
from cbra.types import IDependant
from cbra.types import OIDCRequestPrincipal
from cbra.types import RFC9068RequestPrincipal
from cbra.types import SessionRequestPrincipal
from cbra.types import JSONWebToken
from ..ioc.config import TRUSTED_AUTHORIZATION_SERVERS
from ..params import ApplicationSecretKey
from ..secretkey import SecretKey


class AuthenticationService(
    ICredentialVerifier[RFC9068RequestPrincipal|OIDCRequestPrincipal|SessionRequestPrincipal],
    IDependant
):
    __module__: str = 'cbra.core.iam'
    providers: set[str]

    def __init__(
        self,
        providers: list[str] = TRUSTED_AUTHORIZATION_SERVERS,
        secret_key: SecretKey = ApplicationSecretKey
    ):
        self.providers = set(providers)
        self.secret_key = secret_key

    @functools.singledispatchmethod # type: ignore
    async def verify(
        self,
        principal: OIDCRequestPrincipal | RFC9068RequestPrincipal | SessionRequestPrincipal,
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
        principal: OIDCRequestPrincipal,
        credential: JSONWebToken,
        providers: set[str] | None = None
    ) -> bool:
        return await self.verify_oauth_jwt(principal, credential, providers)

    async def verify_oauth_jwt(
        self,
        principal: OIDCRequestPrincipal | RFC9068RequestPrincipal,
        credential: JSONWebToken,
        providers: set[str] | None = None
    ) -> bool:
        providers = providers or self.providers
        if principal.iss not in providers:
            return False
        async with Client(issuer=principal.iss) as client:
            return await client.verify(str(credential))

    @verify.register
    async def verify_session(
        self,
        principal: SessionRequestPrincipal,
        credential: HMACSignature,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        return await credential.verify(self.secret_key)