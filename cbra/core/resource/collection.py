# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.types import IQueryResult
from .resourcemodel import ResourceModel


class Collection:
    __module__: str = 'cbra.core'
    cursor_param_name: str = '_c'
    model: type[ResourceModel]

    async def list(self) -> Any:
        result = await self.filter(None)
        resource =  self.model.__list_model__.parse_obj({
            'apiVersion': 'v1',
            'kind': f'{self.model.__name__}List',
            'metadata': {
                'nextUrl': self.get_next_url(result.token)
            },
            'items': []
        })
        resource.items = [self.adapt(x) for x in result.items] # type: ignore
        return resource

    async def filter(self, params: Any) -> IQueryResult[Any]:
        raise NotImplementedError
    
    def get_next_url(self, token: str | None) -> str | None:
        if not token:
            return None
        return self.reverse('list', params={self.cursor_param_name: token}) # type: ignore