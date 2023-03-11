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
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import TypeVar

import pydantic
from headless.ext.oauth2.types import GrantType

from ..types import RefreshTokenPolicyType
from ..types import RefreshTokenType
from ..types import RefreshTokenStatus


T = TypeVar('T', bound='RefreshToken')


class RefreshToken(pydantic.BaseModel):
    created: datetime
    client_id: str
    granted: datetime
    grant_id: int = 0
    grant_type: GrantType
    expires: datetime
    ppid: int
    renew: RefreshTokenPolicyType
    scope: set[str]
    sector_identifier: str
    status: RefreshTokenStatus = RefreshTokenStatus.active
    sub: int
    ttl: int
    token: RefreshTokenType

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        expires = values.get('expires')
        created = values.setdefault('created', datetime.now(timezone.utc))
        ttl = values.get('ttl')
        values.setdefault('granted', created)
        if ttl is not None and not expires:
            assert isinstance(ttl, int)
            values['expires'] = created + timedelta(seconds=ttl)
        if not values.get('token'):
            values['token'] = RefreshTokenType(secrets.token_urlsafe(48))
        return values

    def refresh(self: T) -> T:
        """Refresh the token."""
        now = datetime.now(timezone.utc)
        obj = type(self).parse_obj({
            **self.dict(),
            'created': now,
            'token': RefreshTokenType(secrets.token_urlsafe(48))
        })
        if obj.renew == RefreshTokenPolicyType.rolling:
            obj.expires = now + timedelta(seconds=self.ttl)
        elif obj.renew == RefreshTokenPolicyType.static:
            obj.expires = self.expires
        else:
            raise NotImplementedError
        self.status = RefreshTokenStatus.consumed
        return obj

    def can_use(self, scope: set[str]) -> bool:
        return scope <= self.scope
    
    def is_active(self) -> bool:
        return self.status == RefreshTokenStatus.active