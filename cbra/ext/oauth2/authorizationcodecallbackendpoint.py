# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
.. _ref-guides-integrating-an-oauth2-authorization-server

=============================================
Integrating an OAuth 2.x authorization server
=============================================
"""
import fastapi
from headless.ext import oauth2

import cbra.core as cbra
from cbra.core.conf import settings
from .types import RedirectParameters


class AuthorizationCodeCallbackEndpoint(cbra.Endpoint):
    """Handles a redirect from an OAuth 2.x/OpenID Connect
    authorization server.
    """
    __module__: str = 'cbra.ext.oauth2'
    status_code: int = 303
    summary: str = 'Redirection Endpoint'
    tags: list[str] = ['OAuth 2.x/OpenID Connect']

    async def get(
        self,
        client_id: str,
        params: RedirectParameters = RedirectParameters.depends()
    ):
        client = await self.get_client(client_id)
        if client is None:
            return fastapi.responses.PlainTextResponse(
                content=f"The client {client_id} is not configured for this server."
            )
        async with client:
            at = await params.obtain(
                client,
                redirect_uri=(
                    f'{self.request.url.scheme}://'
                    f'{self.request.url.netloc}{self.request.url.path}'
                )
            )
            await self._on_success(client, at)

    async def _on_success(
        self,
        client: oauth2.Client,
        at: oauth2.TokenResponse
    ) -> None:
        raise NotImplementedError(at)

    async def get_client(self, client_id: str) -> oauth2.Client | None:
        """Return a preconfigured OAuth 2.x/OpenID Connect client,
        or ``None`` if the client does not exist.
        """
        # TODO: Quite ugly
        for client in settings.OAUTH2_CLIENTS:
            if client_id in {client.get('name'), client.get('client_id')}:
                instance = oauth2.Client(**client)
                break
        else:
            instance = None
        return instance