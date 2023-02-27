# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
from typing import TypeVar

import pydantic

from .ihashable import IHashable
from .sessionclaims import SessionClaims


T = TypeVar('T', bound='SessionModel')


class SessionModel(pydantic.BaseModel, IHashable):
    id: str
    iat: int
    claims: SessionClaims | None = None
    hmac: str | None = None

    @classmethod
    def parse_cookie(cls: type[T], value: str | None) -> T | None:
        if value is None: return None
        try:
            serialized = base64.urlsafe_b64decode(str.encode(value, 'ascii'))
            return cls.parse_raw(serialized)
        except Exception:
            return None

    def digest(self) -> bytes:
        return self._hash(self.dict(exclude={'hmac'}, exclude_none=True))