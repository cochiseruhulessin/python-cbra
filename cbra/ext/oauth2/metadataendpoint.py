# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.ext.oauth2.models import ServerMetadata

from .endpoint import AuthorizationServerEndpoint
from .params import CurrentIssuer


class MetadataEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    issuer: str = CurrentIssuer
    name: str = 'oauth2.metadata'
    path: str = '/.well-known/oauth-authorization-server'
    summary: str = 'Metadata Endpoint'

    async def get(self) -> ServerMetadata:
        return ServerMetadata(
            issuer=self.issuer,
            authorization_endpoint=str(self.request.url_for('oauth2.authorize')),
            token_endpoint=str(self.request.url_for('oauth2.token'))
        )