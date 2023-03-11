# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from .danceinitiationmixin import DanceInitiationMixin
from .tokenhandlerendpoint import TokenHandlerEndpoint


class FrontendLoginEndpoint(TokenHandlerEndpoint, DanceInitiationMixin):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'bff.login'
    path: str = '/bff/login'
    redirection_endpoint: str = 'bff.redirection'
    status_code: int = 303
    summary: str = 'Frontend Login Endpoint'

    async def get(self) -> fastapi.Response:
        """Retrieve an OIDC ID Token from the trusted authorization
        server to establish the identity of the caller.
        """
        url, state, nonce = await self.create_authorization_request(
            scope={'email', 'openid', 'profile'},
            access_type='offline'
        )
        self.set_cookie('nonce', nonce)
        self.set_cookie('state', state)
        return fastapi.responses.RedirectResponse(
            status_code=303,
            url=url
        )