# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import cbra.core as cbra
from cbra.types import Request
from .basestorage import BaseStorage
from .models import AuthorizationServerModel
from .models import Client


T = TypeVar('T', bound=AuthorizationServerModel)


class ApplicationStorage(BaseStorage):
    """A :class:`~cbra.ext.oauth2.BaseStorage` implementation that
    retrieves specific resources from either environment variables,
    local configuration files, or the :mod:`~cbra.core.conf.settings`
    module.
    """
    __module__: str = 'cbra.ext.oauth2'
    client: Client | None

    def __init__(
        self,
        request: Request,
        client: dict[str, Any] = cbra.instance('_LocalClient')
    ) -> None:
        self.client = None
        if client:
            self.client = Client.parse_obj({
                **client,
                'client_id': 'self',
                'kind': 'Application',
            })

    async def get(self, cls: type[T], *args: Any, **kwargs: Any) -> T | None:
        if cls == Client:
            return await super().get(cls, *args, **kwargs)
        else:
            return None
        
    async def get_client(self, client_id: str) -> Client | None:
        if client_id != 'self':
            return None
        return self.client