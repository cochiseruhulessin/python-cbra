# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.types import IEndpoint
from .persister import Persister
from .resourcemodel import ResourceModel


class IResource(IEndpoint, Persister):
    model: type[ResourceModel]
    path_name: str
    response_model_by_alias: bool = False
    resource_name: str
    resource_id: Any
    verbose_name: str
    verbose_name_plural: str

    async def get_object(self) -> Any:
        raise NotImplementedError