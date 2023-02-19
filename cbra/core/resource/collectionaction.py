# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .resourceaction import ResourceAction


class CollectionAction(ResourceAction):
    __module__: str = 'cbra.core.resource'

    def is_detail(self) -> bool:
        return False

    def get_return_annotation(self) -> Any:
        return self.endpoint.model.__list_model__