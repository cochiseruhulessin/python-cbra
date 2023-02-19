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

import fastapi
import pydantic

from cbra.types import IEndpoint
from .resourceaction import ResourceAction


T = TypeVar('T', bound='CreateAction')


class CreateAction(ResourceAction):
    action: str = 'create'
    name_template: str = 'Create a new {name}'
    status_code: int = 201

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        return cls(name=name, method='POST', func=func)

    def can_write(self) -> bool:
        return True

    def get_return_annotation(self) -> Any:
        return self.endpoint.model.__response_model__

    def get_openapi_responses(
        self,
        responses: dict[int | str, Any]
    ) -> dict[int | str, Any]:
        responses.update({
            409: {
                'description': (
                    'The unique properties of an existing '
                    f'**{self.endpoint.verbose_name}** conflict'
                )
            }
        })
        return super().get_openapi_responses(responses)

    def get_write_model(self) -> type[pydantic.BaseModel]:
        return self.endpoint.model.__create_model__

    def is_detail(self) -> bool:
        return False

    def parse_resource(self, resource: pydantic.BaseModel) -> pydantic.BaseModel:
        return self.endpoint.model.parse_obj(resource.dict())

    async def process_response(
        self,
        endpoint: IEndpoint,
        response: fastapi.Response | pydantic.BaseModel | None
    ) -> fastapi.Response | pydantic.BaseModel | None:
        if isinstance(response, pydantic.BaseModel):
            response = self.response_model.parse_obj(response.dict())
        return await super().process_response(endpoint, response)