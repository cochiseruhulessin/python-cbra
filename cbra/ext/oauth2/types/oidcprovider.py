# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic
from headless.ext import oauth2
from headless.ext.oauth2.models import AuthorizationEndpointResponse
from headless.ext.oauth2.models import TokenResponse

from .clientsecret import ClientSecret
from .fatalauthorizationexception import FatalAuthorizationException


class OIDCProvider(pydantic.BaseModel):
    """A downstream OpenID Connect provider."""
    protocol: Literal['oidc']
    name: str
    issuer: str
    scope: set[str] = set()
    credential: ClientSecret
    params: dict[str, Any] = {}
    _client: oauth2.Client | None = pydantic.PrivateAttr(None)

    @property
    def client_id(self) -> str:
        return self.credential.client_id

    async def get_redirect_uri(
        self,
        redirect_uri: str,
        state: str,
        nonce: str
    ) -> str:
        assert self._client is not None
        return await self._client.authorize(
            state=state,
            redirect_uri=redirect_uri,
            scope=self.scope,
            nonce=nonce,
            prompt='select_account'
        )
    
    async def obtain(self, code: str, state: str, redirect_uri: str):
        assert self._client is not None
        response = AuthorizationEndpointResponse.parse_obj({
            'code': code,
            'state': state
        })
        return await self._client.token(
            response.__root__,
            redirect_uri=redirect_uri
        )
    
    async def verify(self, response: TokenResponse, nonce: str | None = None):
        assert self._client is not None
        await self._client.verify_response(response)
        if response.id_token:
            if not nonce:
                raise TypeError(
                    "The 'nonce' parameter is required if an ID token is "
                    "requested."
                )
            if not await self._client.verify_oidc(response.id_token, nonce=nonce):
                raise FatalAuthorizationException(
                    "The ID token in the response from the authorization server "
                    "did not validate."
                )

    async def __aenter__(self):
        self._client = oauth2.Client(
            issuer=self.issuer,
            client_id=self.credential.client_id,
            client_secret=self.credential.client_secret,
            params=self.params
        )
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any):
        assert self._client is not None
        return await self._client.__aexit__(*args, **kwargs)