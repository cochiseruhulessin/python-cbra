# Copyright (C) 2021-2023 Cochise Ruhulessin
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
from typing import Generic
from typing import TypeVar

from .sessionclaims import SessionClaims


C = TypeVar('C', bound=SessionClaims)
T = TypeVar('T', bound='ISessionData[Any]')


class ISessionData(Generic[C]):
    claims: C | None

    @classmethod
    def parse_cookie(cls: type[T], value: str) -> T | None:
        raise NotImplementedError

    def as_cookie(self) -> str:
        raise NotImplementedError

    def get(self, key: str) -> Any:
        raise NotImplementedError

    def set(self, key: str, value: Any) -> bool:
        """Set the value and return a boolean indicating if the data
        was modified.
        """
        raise NotImplementedError

    def update(self, claims: dict[str, Any]) -> None:
        raise NotImplementedError

    async def sign(
        self,
        sign: Callable[[bytes], Awaitable[str]]
    ) -> None:
        raise NotImplementedError

    async def verify(
        self,
        verify: Callable[[bytes | str, bytes], Awaitable[bool]]
    ) -> bool:
        raise NotImplementedError