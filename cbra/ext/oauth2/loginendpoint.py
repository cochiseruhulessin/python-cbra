# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import fastapi
from headless.ext import oauth2

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.types import Forbidden
from cbra.types import NotFound
from .endpoint import AuthorizationServerEndpoint
from .types import LoginResponse
from .models import AuthorizationState


class LoginEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'oauth2.login'
    nonce_cookie_name: str = 'oidc.nonce'
    redirect_cookie_name: str = 'oauth2.redirect-uri'
    state_cookie_name: str = 'oauth2.state'
    status_code: int = 303
    summary: str = 'Login Endpoint'
    tags: list[str] = ['OAuth 2.x/OpenID Connect']

    async def get(
        self,
        success_url: str | None = fastapi.Query(
            default=None,
            title='Next URL',
            alias='next',
            description=(
                'The URL to which the server must redirect the user-agent '
                'after a successful login. If this value is not provided '
                'then the server may use a default URL.'
            )
        ),
        client_id: str = fastapi.Path(
            default=...,
            title='Client ID',
            description=(
                'The OAuth 2.x/OpenID Connect client to initiate the '
                'authorization flow with. If not provided, the server '
                'may select a default client.'
            )
        )
    ) -> fastapi.responses.RedirectResponse:
        """Initiate the authorization code flow by redirecting the user agent
        to the authorization servers' authorization endpoint.
        """
        success_url = success_url or '/'
        if not self.can_redirect(success_url):
            raise Forbidden
        if self.ctx.is_authenticated():
            return fastapi.responses.RedirectResponse(
                status_code=303,
                url=success_url
            )

        client = await self.get_client(client_id)
        if client is None:
            raise NotFound
        params = AuthorizationState.new(redirect_uri=success_url)
        redirect_uri = self.request.url_for('oauth2.callback', client_id=client_id)
        async with client:
            url = await client.authorize(
                state=params.state,
                redirect_uri=redirect_uri,
                scope={'openid', 'email'},
                nonce=params.nonce,
                prompt='select_account'
            )

        # Persist the state so that the callback endpoint can find the needed
        # information to forward the request.
        await self.storage.persist(params)
        return fastapi.responses.RedirectResponse(
            status_code=self.status_code,
            url=url
        )

    @cbra.describe(status_code=200)
    async def post(
        self,
        client_id: str = fastapi.Path(
            default=...,
            title='Client ID',
            description=(
                'The OAuth 2.x/OpenID Connect client to initiate the '
                'authorization flow with. If not provided, the server '
                'may select a default client.'
            )
        )
    ) -> LoginResponse:
        """Initiate the authorization code flow and return a JSON object
        containing information on how to proceed.
        """
        client = await self.get_client(client_id=client_id)
        if client is None:
            raise NotFound
        raise NotImplementedError

    def can_redirect(self, redirect_uri: str) -> bool:
        """Return a boolean if the user-agent may request a redirect to the
        given URI.
        """
        p = urllib.parse.urlparse(redirect_uri)
        return any([
            str.startswith(redirect_uri, '/'),
            all([
                p.netloc == self.request.url.netloc,
                p.scheme == self.request.url.scheme,
            ]),
            p.netloc in settings.LOGIN_AUTHORIZED_DOMAINS
        ])

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