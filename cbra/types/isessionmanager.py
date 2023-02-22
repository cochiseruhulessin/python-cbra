# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
from typing import Any
from typing import Generic
from typing import TypeVar

import fastapi

from .isessiondata import ISessionData
from .sessionclaims import SessionClaims


M = TypeVar('M', bound=ISessionData[Any])


class ISessionManager(Generic[M]):
    __module__: str = 'cbra.types'
    dirty: bool = False
    data: M

    @property
    def claims(self) -> SessionClaims:
        # Ensure that the user does not circumvent the setter.
        return copy.deepcopy(self.data.claims or SessionClaims())

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        self.dirty = self.data.set(key, value)

    def update(self, claims: dict[str, Any]) -> None:
        self.dirty = True
        self.data.update(claims)

    def is_dirty(self) -> bool:
        return self.dirty

    async def add_to_response(self, response: fastapi.Response) -> None:
        """Update a response to include the session."""
        raise NotImplementedError

    async def clear(self) -> None:
        raise NotImplementedError