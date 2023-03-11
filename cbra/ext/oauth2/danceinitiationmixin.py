# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from typing import Any

from cbra.types import Request
from headless.ext.oauth2 import Client


class DanceInitiationMixin:
    __module__: str = 'cbra.ext.oauth2'
    client: Client
    cookie_prefix: str
    redirection_endpoint: str
    request: Request

    async def create_authorization_request(
        self,
        scope: set[str],
        state: str | None = None,
        redirect_uri: str | None = None,
        **params: Any
    ) -> tuple[str, str, str]:
        state = state or secrets.token_urlsafe(48)
        nonce = secrets.token_urlsafe(48)
        return await self.client.authorize(
            redirect_uri=redirect_uri or self.get_redirect_uri(),
            state=state,
            nonce=nonce,
            scope=scope,
            **params
        ), state, nonce
    
    def get_redirect_uri(self) -> str:
        return str(self.request.url_for(self.redirection_endpoint))