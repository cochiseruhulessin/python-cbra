# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import Literal

import pydantic
from headless.ext.oauth2.models import TokenResponse
from headless.ext.oauth2.types import GrantType

from cbra.core.iam.models import Subject
from ..types import AuthorizationCode
from ..types import ITokenBuilder
from ..types import ITokenSigner
from .authorizationrequest import AuthorizationRequest
from .client import Client
from .resourceowner import ResourceOwner


class AuthorizationCodeGrant(pydantic.BaseModel):
    code: AuthorizationCode
    client: Client
    grant_type: Literal[GrantType.authorization_code]
    owner: ResourceOwner
    redirect_uri: str | None = None
    request: AuthorizationRequest
    subject: Subject

    @pydantic.validator('request')
    def validate_request(
        cls,
        request: AuthorizationRequest | None
    ) -> AuthorizationRequest:
        if request is None:
            raise ValueError('authorization request missing.')
        if not request.has_owner():
            raise ValueError('authorization request does not have an owner.')
        return request
    
    @pydantic.root_validator
    def validate_grant(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        client = cast(Client, values.get('client'))
        owner = cast(ResourceOwner, values.get('owner'))
        redirect_uri = cast(str, values.get('redirect_uri'))
        request = cast(AuthorizationRequest, values.get('request'))
        is_valid: bool = all([
            client,
            request,
            redirect_uri,
            owner
        ])
        if not is_valid:
            return values

        if not request.is_owned_by(owner.sub):
            raise ValueError('request was made by a different Subject.')

        if redirect_uri != request.redirect_uri:
            raise ValueError(
                'redirect URI does not correspond with the redirect URI '
                'requested.'
            )

        return values
    
    async def create_response(
        self,
        builder: ITokenBuilder,
        signer: ITokenSigner
    ) -> TokenResponse:
        assert self.owner.ppid.value is not None
        at, expires_in = builder.rfc9068(
            sub=self.owner.ppid.value,
            scope=self.request.scope,
            auth_time=self.request.auth_time
        )
        id_token = None
        refresh_token = None
        if self.request.has_refresh_token():
            refresh_token = await builder.refresh_token(
                grant_type=GrantType.authorization_code,
                client_id=self.client.client_id,
                sector_identifier=self.client.sector_identifier,
                sub=self.owner.sub,
                ppid=self.owner.ppid.value,
                scope=self.request.scope,
                renew=self.client.refresh_token_policy,
                ttl=self.client.refresh_token_ttl
            )
        return TokenResponse.parse_obj({
            'token_type': 'Bearer',
            'access_token': await at.sign(signer),
            'expires_in': expires_in,
            'id_token': id_token,
            'refresh_token': refresh_token
        })