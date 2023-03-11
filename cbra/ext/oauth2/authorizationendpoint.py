# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
import urllib.parse

import fastapi

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.types import SessionRequestPrincipal
from .endpoint import AuthorizationServerEndpoint
from .models import AuthorizationRequestClient
from .models import AuthorizationRequest
from .models import ResourceOwner
from .types import ResourceOwnerIdentifier


class AuthorizationEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    client: AuthorizationRequestClient # type: ignore
    metrics: cbra.MetricReporter = cbra.MetricReporter('oauth2')
    name: str = 'oauth2.authorize'
    principal: SessionRequestPrincipal # type: ignore
    path: str = '/authorize'
    status_code: int = 303
    summary: str = 'Authorization Endpoint'

    async def get(
        self,
        params: AuthorizationRequest = AuthorizationRequest.depends()
    ) -> fastapi.Response:
        await self.session
        await params.load(
            client=self.client,
            storage=self.storage,
            session_id=self.session.id
        )

        # First check if the client requires authentication with a
        # downstream provider, since the user will be authenticated
        # any way when it returns here.
        if self.client.requires_downstream() and not params.is_authenticated():
            return await self.on_downstream_required(params)

        if not self.is_authenticated():
            return await self.on_login_required(params)
        assert self.session.uid
        owner, created = await self.get_or_create_resource_owner(
            client=self.client,
            subject_id=self.session.uid
        )
        if created:
            self.logger.debug(
                "Onboarded subject to client (client: %s, "
                "sub: %s, sector: %s, ppid: %s)",
                self.client.client_id, self.session.uid,
                owner.ppid.sector, owner.ppid.value
            )
        await params.verify(self.session.claims, self.client, owner.sub)
        await params.persist(self.storage)
        self.delete_cookies()
        return params.as_response(client=self.client, iss=self.get_issuer())

    async def on_downstream_required(
        self,
        params: AuthorizationRequest
    ) -> fastapi.Response:
        """Invoked when the end-user must authenticate with a downstream
        identity provider.
        """
        self.logger.debug(
            "Client requires downstream authentication (client_id: %s)",
            self.client.client_id
        )
        state = params.id
        nonce = secrets.token_urlsafe(48)
        async with self.client.get_provider() as provider:
            url = await provider.get_redirect_uri(
                redirect_uri=str(self.request.url_for('oauth2.callback')),
                state=state,
                nonce=nonce
            )
        response = fastapi.responses.RedirectResponse(
            status_code=303,
            url=url
        )
        response.set_cookie(key='oauth2.client_id', value=self.client.client_id)
        response.set_cookie(key='oauth2.nonce', value=nonce)
        response.set_cookie(key='oauth2.request', value=params.id)
        response.set_cookie(key='oauth2.state', value=params.id)
        return response

    async def on_login_required(self, params: AuthorizationRequest) -> fastapi.Response:
        """Invoked when the end-user needs to establish an authenticated
        session before proceeding with an authorization request.
        """
        p: dict[str, str] = {
            'next': params.get_authorize_url(self.request),
            'request': params.id
        }
        q = urllib.parse.urlencode(p, quote_via=urllib.parse.quote)
        return fastapi.responses.RedirectResponse(
            status_code=303,
            url=settings.LOGIN_URL + f'?{q}'
        )

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
    
    async def get_or_create_resource_owner(
        self,
        client: AuthorizationRequestClient,
        subject_id: int
    ) -> tuple[ResourceOwner, bool]:
        created = False
        owner = await self.storage.get(
            ResourceOwner,
            ResourceOwnerIdentifier(client_id=client.client_id, sub=subject_id)
        )
        if owner is None:
            created = True
            ppid = client.get_pairwise_identifier(subject_id)
            await self.storage.persist(ppid)
            owner = ResourceOwner(
                client_id=client.client_id,
                ppid=ppid,
            )
            await self.storage.persist(owner)
            self.metrics.report('SubjectOnboarded', {
                'client_id': client.client_id,
                'sector_identifier': client.sector_identifier
            })
        return owner, created