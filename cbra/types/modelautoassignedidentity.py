# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import overload
from typing import TypeVar

import pydantic
import pydantic.main


T = TypeVar('T', bound='ModelAutoAssignedIdentity')


class ModelAutoAssignedIdentity:
    """Like :class:`~cbra.types.ModelIdentity`, but for a single field
    that is an auto assigned integer.
    """
    __module__: str = 'cbra.types'
    field: pydantic.fields.FieldInfo
    attname: str

    def __init__(self, attname: str, field: pydantic.fields.FieldInfo):
        self.attname = attname
        self.field = field

    @overload
    def __get__(
        self: T,
        obj: None,
        cls: None
    ) -> T:
        ...

    @overload
    def __get__(
        self,
        obj: pydantic.BaseModel,
        cls: type[pydantic.BaseModel]
    ) -> int:
        ...

    def __get__(
        self: T,
        obj: pydantic.BaseModel | None,
        cls: type[pydantic.BaseModel] | None
    ) -> int | None | T:
        if obj is None:
            return self
        return getattr(obj, self.attname)

    def __set__(self, obj: pydantic.BaseModel, value: int) -> None:
        setattr(obj, self.attname, value)