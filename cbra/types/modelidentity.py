# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
from typing import overload
from typing import Any
from typing import Sequence

import pydantic
import pydantic.main


class ModelIdentity:
    """A set of fields that identify a model instance."""
    __module__: str = 'cbra.types'
    fields: dict[str, pydantic.main.FieldInfo]

    def __init__(self, fields: list[pydantic.main.FieldInfo]):
        self.fields = collections.OrderedDict()
        for field in fields:
            assert 'name' in field.extra
            self.fields[field.extra['name']] = field

    @overload
    def __get__(
        self,
        obj: None,
        cls: None
    ) -> Sequence[tuple[str, Any]]:
        ...

    @overload
    def __get__(
        self,
        obj: pydantic.BaseModel,
        cls: type[pydantic.BaseModel]
    ) -> Sequence[tuple[str, Any]]:
        ...

    def __get__(
        self,
        obj: pydantic.BaseModel | None,
        cls: type[pydantic.BaseModel] | None
    ) -> Sequence[tuple[str, Any]]:
        if obj is None:
            return tuple(map(tuple, self.fields.items()))
        return tuple([(k, getattr(obj, k)) for k in self.fields])