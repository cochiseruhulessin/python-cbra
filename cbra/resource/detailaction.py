# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from inspect import Parameter

import fastapi

from .resourceaction import ResourceAction


class DetailAction(ResourceAction):

    def get_url_pattern(self, prefix: str | None) -> str:
        path = super().get_url_pattern(prefix)
        return f'{path}/{{{str.lower(self.endpoint.resource_name)}_id}}'

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