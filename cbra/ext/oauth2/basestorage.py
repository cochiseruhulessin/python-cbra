# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools

from cbra.types import IDependant
from .models import AuthorizationServerModel
from .models import AuthorizationState


class BaseStorage(IDependant):
    __module__: str = 'cbra.ext.oauth2'

    async def destroy(self, obj: AuthorizationServerModel) -> None:
        raise NotImplementedError

    async def get_state(self, key: str) -> AuthorizationState | None:
        raise NotImplementedError

    @functools.singledispatchmethod
    async def persist(
        self,
        obj: AuthorizationServerModel
    ) -> None:
        raise NotImplementedError
    
    async def persist_state(self, obj: AuthorizationState) -> None:
        raise NotImplementedError

    @persist.register
    async def _persist_state(
        self,
        obj: AuthorizationState
    ) -> None:
        return await self.persist_state(obj)