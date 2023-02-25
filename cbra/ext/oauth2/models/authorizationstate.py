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
from typing import TypeVar

import pydantic
from cbra.types import PersistedModel
from ..types import QueryAuthorizeResponse


T = TypeVar('T', bound='AuthorizationState')


class AuthorizationState(PersistedModel):
    created: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    nonce: str
    redirect_uri: str
    state: str = pydantic.Field(
        default=...,
        primary_key=True
    )

    @classmethod
    def new(cls: type[T], redirect_uri: str) -> T:
        return cls(
            nonce=secrets.token_urlsafe(48),
            redirect_uri=redirect_uri,
            state=secrets.token_urlsafe(48),
        )
    
    def is_valid(self, params: QueryAuthorizeResponse | Any) -> bool:
        return isinstance(params, QueryAuthorizeResponse) and params.state == self.state