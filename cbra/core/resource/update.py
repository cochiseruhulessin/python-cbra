# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

from cbra.types import Forbidden
from cbra.types import NotFound
from .resourcemodel import ResourceModel
from .persister import Persister
from .viewer import Viewer


T = TypeVar('T', bound=ResourceModel)


class Update(Persister, Viewer):
    __module__: str = 'cbra.core'

    async def can_update(
        self,
        old: T,
        new: T
    ) -> bool:
        """Return a boolean indicating if the resource may be updated
        based on semantics. If this method returns ``False``, then
        the request is rejected with the ``403`` status code.
        """
        return True

    async def update(self, resource: T) -> T:
        old = await self.get_object()
        if old is None:
            raise NotFound
        new = await self.perform_update(
            old=old,
            new=resource
        )
        if not await self.can_update(old, new):
            raise Forbidden
        await self.persist(new, create=False)
        return new

    async def perform_update(
        self,
        old: T,
        new: T
    ) -> T:
        return old.merge(new)