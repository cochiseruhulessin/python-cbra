# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.types import NotFound
from .detail import Detail


class Retrieve(Detail):
    __module__: str = 'cbra.core'

    async def retrieve(self, *args: Any) -> Any:
        resource = await self.get_object()
        if resource is None:
            raise NotFound
        return resource