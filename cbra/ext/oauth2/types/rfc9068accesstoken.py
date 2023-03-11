# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

from .itokensigner import ITokenSigner
from .signable import Signable


class RFC9068AccessToken(Signable):
    iss: str
    aud: str| list[str]
    exp: int
    sub: str
    client_id: str
    iat: int
    jti: str
    auth_time: int | None = None
    acr: str = '0'
    amr: list[str] | None = []
    scope: str | None = None

    @classmethod
    def new(
        cls,
        client_id: str,
        iss: str,
        aud: str | set[str] | list[str],
        sub: str,
        now: int,
        ttl: int,
        scope: set[str] | None = None,
        auth_time: int | None = None,
        acr: str = '0',
        amr: list[str] | None = None
    ) -> 'RFC9068AccessToken':
        if isinstance(aud, (list, set)):
            aud = list(sorted(aud))
        
        params: dict[str, int | str | list[str] | None] = {
            'acr': acr,
            'aud': aud,
            'client_id': client_id,
            'exp': now + ttl,
            'iat': now,
            'iss': iss,
            'jti': secrets.token_urlsafe(48),
            'nbf': now,
            'sub': sub,
            'auth_time': auth_time
        }
        if scope is not None:
            params['scope'] = ' '.join(sorted(scope))
        if amr is not None:
            params['amr'] = amr
        return cls.parse_obj(params)
    
    async def sign(self, signer: ITokenSigner) -> str:
        return await signer.jwt(self.dict(exclude_none=True), "at+jwt")