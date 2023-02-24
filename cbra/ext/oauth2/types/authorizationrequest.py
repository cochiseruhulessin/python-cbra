# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar
from typing import Union

import fastapi
import pydantic
from headless.ext.oauth2.types import ResponseMode
from headless.ext.oauth2.types import ResponseType

from cbra.types import IDependant
from cbra.core.ioc import override
from .authorizationrequestobject import AuthorizationRequestObject
from .authorizationrequestreference import AuthorizationRequestReference
from .redirecturi import RedirectURI


T = TypeVar('T', bound='BaseAuthorizationRequest')


class BaseAuthorizationRequest(IDependant, pydantic.BaseModel):

    @classmethod
    def fromrequest(
        cls: type[T],
        client_id: str | None = fastapi.Query(
            default=None,
            title="Client ID",
            description="Identifies the client that is requesting authorization."
        ),
        response_type: ResponseType | None = fastapi.Query(
            default=None,
            title="Response type",
            description=(
                "Informs the authorization server of the desired response type."
            ),
            example="code",
        ),
        redirect_uri: RedirectURI | None = fastapi.Query(
            default=None,
            title="Redirect URI",
            description=(
                "The URL to redirect the client to after completing the "
                "flow. Must be an absolute URI that is served over https.\n\n"
                "If `redirect_uri` is omitted, the default redirect URI for "
                "the client specified by `client_id` is used. For clients that "
                "do not have a redirect URI specified, this produces an error "
                "state."
            )
        ),
        scope: str | None = fastapi.Query(
            default=None,
            title="Scope",
            description=(
                "A space-delimited list specifying the requested access scope."
            ),
            max_length=512,
            example="hello.world"
        ),
        state: str | None = fastapi.Query(
            default=None,
            title="State",
            description=(
                "An opaque value used by the client to maintain state between "
                "the request and callback. The authorization server includes "
                "this value when redirecting the user-agent back to the client."
            ),
            max_length=64,
            example=bytes.hex(os.urandom(64))
        ),
        response_mode: ResponseMode | None = fastapi.Query(
            default=None,
            title="Response mode",
            description=(
                "Informs the authorization server of the mechanism to be used "
                "for returning authorization response parameters."
            ),
            example="query"
        ),
        request: str | None = fastapi.Query(
            default=None,
            title="Request",
            description=(
                "A JSON Web Token (JWT) whose JWT Claims Set holds the "
                "JSON-encoded OAuth 2.0 authorization request parameters. "
                "Must not be used in combination with the `request_uri` "
                "parameter, and all other parameters except `client_id` "
                "must be absent.\n\n"
                "Confidential and credentialed clients must first sign "
                "the claims using their private key, and then encrypt the "
                "result with the public keys that are provided by the "
                "authorization server through the `jwks_uri` specified "
                "in its metadata."
            )
        ),
        request_uri: str | None = fastapi.Query(
            default=None,
            title="Request URI",
            description=(
                "References a Pushed Authorization Request (PAR) or a remote "
                "object containing the authorization request.\n\n"
                "If the authorization request was pushed to this authorization "
                "server, then the format of the `request_uri` parameter is "
                "`urn:ietf:params:oauth:request_uri:<reference-value>`. "
                "Otherwise, it is an URI using the `https` scheme. If the "
                "`request_uri` parameter is a remote object, then the external "
                "domain must have been priorly whitelisted by the client."
            )
        )
    ) -> T:
        raise NotImplementedError

    @classmethod
    def __inject__(cls: type[T]) -> Callable[..., Awaitable[T] | T]:
        return cls.fromrequest


class AuthorizationRequest(BaseAuthorizationRequest):
    __root__: Union[
        AuthorizationRequestReference,
        AuthorizationRequestObject
    ]

    @classmethod
    @override(BaseAuthorizationRequest.fromrequest) # type: ignore
    def fromrequest(cls: type[T], **kwargs: Any) -> T: # type: ignore
        return cls.parse_obj(kwargs)