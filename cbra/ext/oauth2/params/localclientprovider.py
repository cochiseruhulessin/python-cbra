# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.core.conf import settings
from ..types import OIDCProvider


class ClientProvider:
    clients: dict[str, OIDCProvider] = {}

    def __init__(self):
        for client in settings.OAUTH2_CLIENTS:
            provider = OIDCProvider.parse_obj({**client, 'protocol': 'oidc'})
            self.clients[provider.name] = provider

    async def get(self, client_id: str) -> OIDCProvider | None:
        return self.clients.get(client_id)


LocalClientProvider: ClientProvider = fastapi.Depends(ClientProvider)