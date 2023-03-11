# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.ext.oauth2.models import TokenResponse

from .params import FrontendTokenResponse
from .tokenhandlerendpoint import TokenHandlerEndpoint


class FrontendRedirectionEndpoint(TokenHandlerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'bff.redirection'
    path: str = '/bff/callback'
    status_code: int = 303
    summary: str = 'Frontend Redirection Endpoint'
    token: TokenResponse = FrontendTokenResponse

    async def get(self) -> TokenResponse:
        return self.token