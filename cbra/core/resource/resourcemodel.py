# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

import pydantic

from .resourceidentifier import ResourceIdentifier
from .resourcemodeltype import ResourceModelType


T = TypeVar('T', bound='ResourceModel')


class ResourceModel(pydantic.BaseModel, metaclass=ResourceModelType):
    __abstract__: bool = True
    __create_model__: type[pydantic.BaseModel]
    __update_model__: type[pydantic.BaseModel]
    __replace_model__: type[pydantic.BaseModel]
    __response_model__: type[pydantic.BaseModel]
    __list_model__: type[pydantic.BaseModel]
    __key_model__: type[ResourceIdentifier]

    def can_replace(self) -> bool:
        raise NotImplementedError

    def merge(self: T, resource: T) -> T:
        return self.parse_obj({
            **self.dict(),
            **resource.dict(
                exclude_defaults=True,
                exclude_none=True,
                exclude_unset=True
            ),
        })