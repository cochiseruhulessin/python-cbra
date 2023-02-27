# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
from typing import Any
from typing import TypeVar

import fastapi
import pydantic
from ckms.utils import b64decode

from .hmacsignature import HMACSignature
from .icredential import ICredential
from .irequestprincipal import IRequestPrincipal
from .sessionclaims import SessionClaims
from .sessionmodel import SessionModel
from .subjectidentifier import SubjectIdentifier


P = TypeVar('P', bound='IRequestPrincipal')


class SessionRequestPrincipal(IRequestPrincipal, ICredential, SessionModel):
    claims: SessionClaims

    @property
    def subject(self) -> SubjectIdentifier | None:
        if not self.claims.iss or not self.claims.sub:
            return None
        return SubjectIdentifier(
            iss=self.claims.iss,
            sub=self.claims.sub
        )

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, fastapi.Request]
    ) -> dict[str, Any]:
        if 'request' in values:
            # TODO: This is ugly but we will figure that out later.
            from cbra.core.conf import settings

            cookie = values['request'].cookies.get(settings.SESSION_COOKIE_NAME)
            if cookie is None:
                raise ValueError('session not provided.')
            try:
                data = base64.urlsafe_b64decode(str.encode(cookie, 'ascii'))
            except (ValueError, TypeError):
                raise
            values = cls.parse_raw(data).dict()
        return values

    def has_audience(self) -> bool:
        return False

    def get_credential(self) -> ICredential | None:
        if self.hmac is not None:
            return HMACSignature(b64decode(self.hmac), self.digest())