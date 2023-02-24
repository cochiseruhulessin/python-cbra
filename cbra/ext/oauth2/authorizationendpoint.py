# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

import cbra.core as cbra
from .endpoint import AuthorizationServerEndpoint
from .types import AuthorizationRequest


class AuthorizationEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'oauth2.authorize'
    status_code: int = 303
    summary: str = 'Authorization Endpoint'
    tags: list[str] = ['OAuth 2.x/OpenID Connect']

    async def get(
        self,
        params: AuthorizationRequest = AuthorizationRequest.depends()
    ) -> fastapi.Response:
        raise NotImplementedError
    
    @cbra.describe(summary="Authorization Endpoint (OpenID Connect)")
    async def post(self) -> None:
        """The OpenID Connect Core specification mandates that the **Authorization
        Endpoint** must support the HTTP `POST` method. This endpoint takes the
        parameters supported by the `GET` endpoint as the request body, which
        must be provided as `application/json` or `application/x-www-form-urlencoded`.

        *This endpoint is not implemented.*
        """
        # https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
        raise NotImplementedError