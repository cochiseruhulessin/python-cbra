# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
from typing import TypeVar

from .basestorage import BaseStorage
from .models import AuthorizationState
from .models import AuthorizationServerModel


T = TypeVar('T')


class MemoryStorage(BaseStorage):
    """An in-memory implementation of :class:`~cbra.ext.oauth2.BaseStorage`."""
    __module__: str = 'cbra.ext.oauth2'
    objects: dict[str, dict[str, AuthorizationServerModel]] = collections.defaultdict(dict)

    @classmethod
    def clear(cls) -> None:
        cls.objects = collections.defaultdict(dict)

    def __init__(self):
        self.objects = MemoryStorage.objects

    async def destroy(self, obj: AuthorizationServerModel) -> None:
        self.objects[type(obj).__name__].pop(obj.__key__[0][1], None) # type: ignore

    async def get_state(self, key: str) -> AuthorizationState | None:
        return self._get(AuthorizationState, key)

    async def persist_state(self, obj: AuthorizationState) -> None:
        self.objects[type(obj).__name__][obj.state] = obj

    def _get(self, Model: type[T], key: str) -> T | None:
        return self.objects[Model.__name__].get(key)