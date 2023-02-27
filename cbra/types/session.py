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

from .isessiondata import ISessionData
from .sessionclaims import SessionClaims
from .sessionmodel import SessionModel


T = TypeVar('T', bound='Session')


class Session(SessionModel, ISessionData[SessionClaims]): # type: ignore

    @classmethod
    def new(cls: type[T]) -> T:
        now = datetime.now(timezone.utc)
        return cls(
            id=secrets.token_urlsafe(48),
            iat=int(now.timestamp())
        )

    def as_cookie(self) -> str:
        assert self.hmac is not None
        v = base64.urlsafe_b64encode(str.encode(self.json(), encoding='utf-8'))
        return bytes.decode(v, 'ascii')

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

    def update(self, claims: dict[str, Any] | SessionClaims) -> None:
        if isinstance(claims, dict):
            claims = SessionClaims.parse_obj(claims)
        if self.claims is None:
            self.claims = SessionClaims()
        self.claims = SessionClaims.parse_obj({
            **self.claims.dict(),
            **claims.dict()
        })
        self.hmac = None

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