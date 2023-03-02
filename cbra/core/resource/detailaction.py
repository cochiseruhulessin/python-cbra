# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from inspect import Parameter
from typing import Any

import fastapi
import pydantic

from cbra.types import IEndpoint
from .iresource import IResource
from .resourceaction import ResourceAction


class DetailAction(ResourceAction):

    def get_url_pattern(
        self,
        prefix: str | None,
        endpoint: type[IResource] | None = None
    ) -> str:
        endpoint = endpoint or self.endpoint
        path = super().get_url_pattern(prefix, endpoint)
        return f'{path}/{{{str.lower(endpoint.resource_name)}_id}}'

    def is_detail(self) -> bool:
        return True

    def preprocess_parameter(self, p: Parameter) -> Parameter | None:
        """Hook to modify a parameter just before it is added to the
        new signature.
        """
        if p.name == self.path_parameter_name:
            return Parameter(
                kind=p.kind,
                name=p.name,
                annotation=p.annotation,
                default=fastapi.Path()
            )
        return super().preprocess_parameter(p)

    def preprocess_signature(
        self,
        parameters: dict[str, Parameter],
        return_annotation: Any
    ):
        if self.path_parameter_name not in parameters:
            parameters[self.path_parameter_name] = Parameter(
                kind=Parameter.POSITIONAL_ONLY,
                name=self.path_parameter_name
            )
        return super().preprocess_signature(parameters, return_annotation)

    async def process_response(
        self,
        endpoint: IEndpoint,
        response: fastapi.Response | pydantic.BaseModel | None
    ) -> fastapi.Response:
        if isinstance(response, pydantic.BaseModel)\
        and not isinstance(response, self.response_model):
            response = self.response_model.parse_obj(response.dict(by_alias=endpoint.response_model_by_alias))
        return await super().process_response(endpoint, response)

    def parse_resource(self, resource: pydantic.BaseModel) -> pydantic.BaseModel:
        parser = self.get_write_model()
        return parser.parse_obj(resource.dict())