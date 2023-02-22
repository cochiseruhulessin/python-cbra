# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar
from typing import Union

import fastapi
import pydantic
from headless.ext import oauth2

from cbra.core.ioc import override
from cbra.types import IDependant
from .jarmauthorizeresponse import JARMAuthorizeResponse
from .queryauthorizeresponse import QueryAuthorizeResponse
from .unsupportedauthorizationresponse import UnsupportedAuthorizationResponse


__all__: list[str] = ['RedirectParameters']
T = TypeVar('T', bound='_RedirectParameters')


class _RedirectParameters(IDependant, pydantic.BaseModel):

    @classmethod
    def fromrequest(
        cls: type[T],
        code: str | None = fastapi.Query(
            default=None,
            title='Authorization code',
            description=(
                'The authorization code generated by the authorization server. '
                'Required if using the Authorization Code Flow and the response '
                'mode is `query`, otherwise this parameter is ignored.'
            )
        ),
        state: str | None = fastapi.Query(
            default=None,
            title='State',
            description=(
                'An opaque value used by the client to maintain state '
                'between the request and callback. The authorization '
                'server includes this value when redirecting the '
                'user-agent back to the client. If supplied, this '
                'parameter **must** equal the `state` parameter used when '
                'creating the authorization request. The `state` parameter '
                'is ignored when using JARM because it is included in the '
                'JSON Web Token supplied using the `jwt` parameter per '
                'chosen response mode.'
            )
        ),
        iss: str | None = fastapi.Query(
            default=None,
            title='Issuer',
            description=(
                'Identifies the authorization server that redirected to '
                'this endpoint, as defined in RFC 9207. If the client supports '
                'OAuth 2.0 Authorization Server Issuer Identification, then '
                'this parameter is **required**, if the response mode is not '
                'JWT Secured Authorization Response Mode (JARM) per RFC 9101.\n\n'
                'The `iss` parameter value is the issuer identifier of '
                'the authorization server that created the authorization '
                'response, as defined in RFC 8414.  Its value **must** '
                'be a URL that uses the `https` scheme without any '
                'query or fragment components.'
            )
        )
    ) -> T:
        raise NotImplementedError

    @classmethod
    def __inject__(cls: type[T]) -> Callable[..., Awaitable[T] | T]:
        return cls.fromrequest


class RedirectParameters(_RedirectParameters):
    __root__: Union[
        QueryAuthorizeResponse,
        JARMAuthorizeResponse,
        UnsupportedAuthorizationResponse
    ]

    @classmethod
    @override(_RedirectParameters.fromrequest) # type: ignore
    def fromrequest(cls: type[T], **kwargs: Any) -> T: # type: ignore
        return cls.parse_obj(kwargs)

    async def obtain(
        self,
        client: oauth2.Client,
        **kwargs: Any
    ) -> oauth2.TokenResponse:
        return await self.__root__.obtain(client, **kwargs)