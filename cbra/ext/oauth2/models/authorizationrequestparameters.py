# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from datetime import datetime
from datetime import timezone
from typing import Any

import fastapi
import pydantic
from headless.ext.oauth2.models import OIDCToken
from headless.ext.oauth2.types import ResponseType

from ..types import AccessType
from ..types import AuthorizationRequestIdentifier
from ..types import RedirectURI
from .authorizationcode import AuthorizationCode
from .authorizationrequestclient import AuthorizationRequestClient


class AuthorizationRequestParameters(pydantic.BaseModel):
    access_type: AccessType = AccessType.online
    client_id: str
    code: AuthorizationCode | None = None
    id: AuthorizationRequestIdentifier | None = None
    response_type: ResponseType
    redirect_uri: RedirectURI
    scope: set[str] = set()
    state: str | None = None

    # Internal properties
    auth_time: int | None = None
    session_id: str | None = None
    downstream: OIDCToken | None = None
    owner: int | None = None
    requested: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    remote_host: str

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        client: AuthorizationRequestClient = values.pop('client', None)
        redirect_uri: RedirectURI | None = values.get('redirect_uri')
        scope: str = values.get('scope') or ''
        if redirect_uri is None and client is not None:
            values['redirect_uri'] = client.get_redirect_uri(redirect_uri)
        if scope and isinstance(scope, str):
            values['scope'] = set(filter(bool, str.split(scope, ' ')))
        return values

    async def load(
        self,
        client: Any,
        storage: Any,
        session_id: str
    ):
        if self.id is None:
            self.id = AuthorizationRequestIdentifier(secrets.token_urlsafe(48))
        if self.issues_authorization_code():
            self.code = AuthorizationCode()
        return self

    def as_response(
        self,
        client: AuthorizationRequestClient,
        issuer: str
    ) -> fastapi.Response:
        assert self.code is not None
        if self.response_type != ResponseType.code:
            raise NotImplementedError
        url = self.redirect_uri.redirect(
            code=self.code.value,
            state=self.state,
            iss=issuer
        )
        assert isinstance(url, str)
        return fastapi.responses.RedirectResponse(
            status_code=303,
            url=url,
        )

    def assign(self, owner: int) -> None:
        """Set the owner for the Authorization Request. This will be used
        later when exchanging the authorization code.
        """
        self.owner = owner

    def issues_authorization_code(self) -> bool:
        return self.response_type in {
            ResponseType.code,
            ResponseType.code_id_token,
            ResponseType.code_id_token_token,
            ResponseType.code_token
        }