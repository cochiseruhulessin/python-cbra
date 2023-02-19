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

from cbra.types import Operation
from .detailaction import DetailAction


T = TypeVar('T', bound='DeleteAction')


class DeleteAction(DetailAction):
    action: str = 'destroy'
    name_template: str = 'Delete {article} {name}'
    response_description: str = 'The deleted **{name}**'

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        return cls(name=name, method='DELETE', func=func)

    def can_write(self) -> bool:
        return False

    def get_openapi_responses(
        self,
        responses: dict[int | str, Any]
    ) -> dict[int | str, Any]:
        responses.update({
            202: {
                'description': (
                    f'The **{self.endpoint.verbose_name}** is scheduled for '
                    'deletion'
                ),
                'model': Operation
            }
        })
        return super().get_openapi_responses(responses)

    def get_return_annotation(self) -> Any:
        return self.endpoint.model.__response_model__ | Operation