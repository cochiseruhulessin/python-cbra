# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
import secrets
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import pydantic

from .isessiondata import ISessionData
from .sessionclaims import SessionClaims


T = TypeVar('T', bound='Session')


class Session(pydantic.BaseModel, ISessionData[SessionClaims]):
    id: str
    iat: int
    claims: SessionClaims | None = None
    hmac: str | None = None

    @classmethod
    def new(cls: type[T]) -> T:
        now = datetime.now(timezone.utc)
        return cls(
            id=secrets.token_urlsafe(48),
            iat=int(now.timestamp())
        )

    @classmethod
    def parse_cookie(cls: type[T], value: str | None) -> T | None:
        if value is None: return None
        try:
            serialized = base64.urlsafe_b64decode(str.encode(value, 'ascii'))
            return cls.parse_raw(serialized)
        except Exception:
            return None

    def as_cookie(self) -> str:
        assert self.hmac is not None
        v = base64.urlsafe_b64encode(str.encode(self.json(), encoding='utf-8'))
        return bytes.decode(v, 'ascii')

    def digest(self) -> bytes:
        return self._hash(self.dict(exclude={'hmac'}, exclude_none=True))

    def set(self, key: str, value: Any) -> bool:
        if self.claims is None:
            self.claims = SessionClaims()
        if key not in self.claims.__fields__:
            raise AttributeError(f'Claim not supported: {key}')
        modified = False
        if getattr(self.claims, key) != value:
            modified = True
            self.hmac = None
            setattr(self.claims, key, value)
        return modified

    async def sign(
        self,
        sign: Callable[[bytes], Awaitable[str]]
    ) -> None:
        self.hmac = await sign(self.digest())

    async def verify(
        self,
        verify: Callable[[bytes | str, bytes], Awaitable[bool]]
    ) -> bool:
        assert self.hmac is not None
        return await verify(self.hmac, self.digest())