# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from .detailaction import DetailAction


T = TypeVar('T', bound='RetrieveAction')


class RetrieveAction(DetailAction):
    action: str = 'retrieve'
    name_template: str = 'Retrieve a single {name}'

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        return cls(name=name, method='GET', func=func)

    def can_write(self) -> bool:
        return False

    def get_return_annotation(self) -> Any:
        return self.endpoint.model.__response_model__