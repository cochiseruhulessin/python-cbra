# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import TypeVar

from cbra.types import Conflict
from .persister import Persister
from .resourcemodel import ResourceModel


T = TypeVar('T', bound=ResourceModel)


class Create:
    __module__: str = 'cbra.core'

    async def can_create(self, resource: Any) -> bool:
        """Return a boolean indicating if the resource may be created
        based on semantics. If this method returns ``False``, then
        the request is rejected with the ``409`` status code.
        """
        raise NotImplementedError

    async def create(self, resource: T) -> T:
        if not await self.can_create(resource):
            raise Conflict
        resource = await self.perform_create(resource)
        return resource

    async def perform_create(self, resource: T) -> T:
        self = cast(Persister, self)
        return await self.persist(resource, create=True)