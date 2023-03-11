# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

import cbra.core as cbra
from ..models import AuthorizationRequest
from ..models import AuthorizationRequestParameters
from ..types import AuthorizationRequestIdentifier
from ..types import FatalAuthorizationException
from ..types import IAuthorizationServerStorage


__all__: list[str] = [
    'CookieStoredAuthorizationRequest'
]


async def get(
    storage: IAuthorizationServerStorage = cbra.instance(
        name='_AuthorizationServerStorage'
    ),
    request_id: AuthorizationRequestIdentifier | None = fastapi.Cookie(
        default=None,
        title="Request ID",
        description=(
            "The local authorization request in which the downstream "
            "authentication takes place."
        ),
        alias='oauth2.request'
    ),
    error: str | None = fastapi.Query(
        default=None,
        title="Error code",
        description=(
            "The error code returned by the authorization server if "
            "the user cancelled the request, refused consent, or "
            "failed to authenticate."
        )
    )
):
    if error:
        return None
    params = None
    if request_id is not None:
        params = await storage.get(AuthorizationRequestParameters, request_id)
    if params is None:
        raise FatalAuthorizationException(
            f"The authorization request (id: {request_id}) does not "
            "exist, is expired, or otherwise not processable."
        )
    authnrequest = AuthorizationRequest.parse_obj(params)
    return authnrequest


CookieStoredAuthorizationRequest: AuthorizationRequest = fastapi.Depends(get)