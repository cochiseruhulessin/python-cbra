# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any

from headless.ext.oauth2.models import TokenResponse

import cbra.core as cbra
from cbra.types import NullRequestPrincipal
from .endpoint import AuthorizationServerEndpoint
from .models import AuthorizationCodeGrant
from .models import Client
from .models import Grant
from .params import RequestingClient
from .params import RequestedGrant
from .params import RequestResourceOwner
from .params import TokenBuilder
from .params import TokenSigner
from .types import ITokenBuilder
from .types import ITokenSigner


class TokenEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    builder: ITokenBuilder = TokenBuilder.depends()
    client: Client = RequestingClient # type: ignore
    metrics: cbra.MetricReporter = cbra.MetricReporter('oauth2')
    name: str = 'oauth2.token'
    summary: str = 'Token Endpoint'
    owner: RequestResourceOwner
    path: str = '/token'
    principal: NullRequestPrincipal = NullRequestPrincipal.depends()
    signer: ITokenSigner = TokenSigner.depends()

    async def post(self, grant: Grant = RequestedGrant) -> TokenResponse:
        return await grant.handle(self.handle_grant)

    @functools.singledispatchmethod
    async def handle_grant(
        self,
        grant: Any
    ) -> TokenResponse:
        raise NotImplementedError(type(grant).__name__)
    
    @handle_grant.register
    async def authorization_code(
        self,
        grant: AuthorizationCodeGrant
    ) -> TokenResponse:
        assert self.request.client is not None
        response = await grant.create_response(self.builder, self.signer)
        self.metrics.report('GrantAuthorized', {
            'client_id': grant.client.client_id,
            'grant_type': grant.grant_type,
            'oidc': bool(response.id_token),
            'refresh_token': bool(response.refresh_token),
            'remote_host': str(self.request.client.host),
            'sector_identifier': grant.client.sector_identifier,
        })
        return response