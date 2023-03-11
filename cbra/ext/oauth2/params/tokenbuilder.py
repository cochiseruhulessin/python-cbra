# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone

from headless.ext.oauth2.types import GrantType

import cbra.core as cbra
from cbra.types import IDependant
from ..authorizationserverstorage import AuthorizationServerStorage
from ..models import Client
from ..models import RefreshToken
from ..types import RefreshTokenPolicyType
from ..types import RFC9068AccessToken
from .currentissuer import CurrentIssuer
from .requestingclient import RequestingClient


class TokenBuilder(IDependant):
    __module__: str = 'cbra.ext.oauth2.params'
    access_token_ttl: int = 3600
    client: Client
    issuer: str
    now: int
    storage: AuthorizationServerStorage

    def __init__(
        self,
        storage: AuthorizationServerStorage = cbra.instance('_AuthorizationServerStorage'),
        issuer: str = CurrentIssuer,
        client: Client = RequestingClient
    ) -> None:
        self.client = client
        self.issuer = issuer
        self.now = int(datetime.now(timezone.utc).timestamp())
        self.storage = storage

    def rfc9068(
        self,
        sub: int,
        scope: set[str],
        auth_time: int,
        audience: str | None = None,
    ) -> tuple[RFC9068AccessToken, int]:
        ttl = self.client.access_token_ttl or self.access_token_ttl
        token = RFC9068AccessToken.new(
            client_id=self.client.client_id,
            iss=self.issuer,
            aud=audience or self.issuer,
            sub=str(sub),
            scope=scope,
            auth_time=auth_time,
            now=self.now,
            ttl=ttl
        )
        return token, ttl

    async def refresh_token(
        self,
        grant_type: GrantType,
        client_id: str,
        sector_identifier: str,
        sub: int,
        ppid: int,
        scope: set[str],
        renew: RefreshTokenPolicyType,
        ttl: int
    ) -> str:
        instance = RefreshToken.parse_obj({
            'grant_type': grant_type,
            'client_id': client_id,
            'sector_identifier': sector_identifier,
            'sub': sub,
            'ppid': ppid,
            'scope': scope,
            'renew': renew,
            'ttl': ttl
        })
        await self.storage.persist(instance)
        return instance.token