# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

import fastapi

import cbra.core as cbra
from ..authorizationserverstorage import AuthorizationServerStorage
from ..models import Client
from ..types import ClientAuthenticationMethod
from ..types import FatalClientException


__all__: list[str] = [
    'RequestingClient'
]


async def get(
    storage: AuthorizationServerStorage = cbra.instance('_AuthorizationServerStorage'),
    client_id: str | None = fastapi.Form(
        default=None,
        title="Client ID",
        description=(
            "**Required**, if the client is not authenticating with the "
            "authorization server or the chosen method of authentication is "
            "`client_secret_post`, `client_secret_jwt`, or `private_key_jwt`, "
            "otherwise this parameter is ignored."
        )
    ),
    client_secret: str | None = fastapi.Form(
        default=None,
        title="Client secret",
        description=(
            "The client-side secret. **Required** if the client is confidential and "
            "authenticates using `client_secret_post`."
        )
    )
) -> Client:
    if client_id is None:
        raise NotImplementedError
    client = await storage.get(Client, client_id)
    if client is None:
        raise FatalClientException(
            code='invalid_client',
            message='The client does not exist.'
        )
    if client.auth_method != ClientAuthenticationMethod.post:
        raise NotImplementedError
    # TODO: This is highly specific for client_secret_post
    if client.is_confidential() and not client_secret:
        raise FatalClientException(
            code='invalid_client',
            message="The 'client_secret' parameter is mandatory for this client."
        )
    if not secrets.compare_digest(client.client_secret or '', client_secret or ''):
        raise FatalClientException(
            code='invalid_client',
            message="The provided client secret is not valid."
        )

    return client


RequestingClient: Client = fastapi.Depends(get)