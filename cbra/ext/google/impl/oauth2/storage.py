# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.google import DatastoreRepository
from cbra.ext.oauth2 import BaseStorage
from cbra.ext.oauth2.models import AuthorizationState
from cbra.types import PersistedModel


class Storage(BaseStorage, DatastoreRepository):
    __module__: str = 'cbra.ext.google.impl.oauth2'

    async def destroy(self, obj: PersistedModel) -> None:
        return await self.delete(self.model_key(obj))

    async def get_state(self, key: str) -> AuthorizationState | None:
        return await self.get_model_by_key(AuthorizationState, key)

    async def persist_state(self, obj: AuthorizationState) -> None:
        await self.put(obj)