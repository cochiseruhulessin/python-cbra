# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from headless.ext import oauth2

from cbra.core.conf import settings
from .endpoint import AuthorizationServerEndpoint
from .types import RedirectParameters
from .types import ResponseValidationFailure
from .types import QueryAuthorizeResponse


class AuthorizationCodeCallbackEndpoint(AuthorizationServerEndpoint):
    """Handles a redirect from an OAuth 2.x/OpenID Connect
    authorization server.
    """
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'oauth2.callback'
    nonce_cookie_name: str = 'oidc.nonce'
    redirect_cookie_name: str = 'oauth2.redirect-uri'
    state_cookie_name: str = 'oauth2.state'
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
        result = params.result()
        if not isinstance(result, QueryAuthorizeResponse):
            raise NotImplementedError
        if result.state is None:
            return fastapi.responses.PlainTextResponse(
                content="This server requires the 'state' parameter."
            )
        req = await self.storage.get_state(result.state)
        if req is None or not req.is_valid(result):
            return fastapi.responses.PlainTextResponse(content="The request is expired.")
        async with client:
            at = await params.obtain(
                client,
                redirect_uri=(
                    f'{self.request.url.scheme}://'
                    f'{self.request.url.netloc}{self.request.url.path}'
                ),
                state=req.state
            )
            await client.verify_response(at)
            if at.id_token and not await client.verify_oidc(at.id_token, nonce=req.nonce):
                raise ResponseValidationFailure("Invalid OIDC token in response.")
            await self.storage.destroy(req)
            await self._on_success(client, at)
        return fastapi.responses.RedirectResponse(
            status_code=303,
            url=req.redirect_uri or '/'
        )

    async def _on_success(
        self,
        client: oauth2.Client,
        at: oauth2.TokenResponse,
    ) -> None:
        id_token = None
        if at.id_token is not None:
            id_token = oauth2.OIDCToken.parse_jwt(
                token=at.id_token,
                email_verified=client.trust_email
            )
        await self.on_success(client, at.access_token, id_token=id_token)

    async def on_success(
        self,
        client: oauth2.Client,
        access_token: oauth2.BearerTokenCredential,
        id_token: oauth2.OIDCToken | None = None
    ) -> None:
        """Obtained when a valid response with a valid, usable token was
        received from the authorization server.
        """
        raise NotImplementedError

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