# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from headless.ext.oauth2.types import GrantType

from .refreshtokenpolicytype import RefreshTokenPolicyType
from .rfc9068accesstoken import RFC9068AccessToken


class ITokenBuilder(Protocol):
    __module__: str = 'cbra.ext.oauth2.types'

    def rfc9068(
        self,
        sub: int,
        scope: set[str],
        auth_time: int,
        audience: str | None = None,
    ) -> tuple[RFC9068AccessToken, int]:
        ...

    async def refresh_token(
        self,
        grant_type: GrantType,
        client_id: str,
        sector_identifier: str,
        sub: int,
        ppid: int,
        scope: set[str],
        renew: RefreshTokenPolicyType,
        ttl: int,
    ) -> str:
        ...