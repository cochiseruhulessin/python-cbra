# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from types import NotImplementedType
from typing import Any
from typing import TypeVar

import pydantic
import pydantic.main

from .modelidentity import ModelIdentity
from .modelautoassignedidentity import ModelAutoAssignedIdentity


T = TypeVar('T', bound='BaseModel')


class BaseModelMetaclass(pydantic.main.ModelMetaclass):
    """Adds some additional features to a :mod:`pydantic` model:
    
    * Fields accept the ``primary_key`` argument, indicating that the
      field is part of the identity of a model.
    * Fields accept the ``auto_assign`` argument, indicating that the
      field may be auto assigned by, for example, a storage backend.
      This is only supported for :class:`int` fields.
    """
    __abstract__: bool
    __module__: str = 'cbra.types'

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> 'BaseModel':
        for b in bases:
            if isinstance(b, BaseModelMetaclass) and not b.__abstract__:
                raise NotImplementedError("Subclassing is not implemented.")

        # Collect the surrogate key, if defined. Multiple surrogate
        # keys are an error.
        if '__surrogate__' in namespace:
            raise TypeError(f'{name}.__surrogate__ must not be declared.')
        namespace.setdefault('__surrogate__', NotImplemented)
        for attname, value in namespace.items():
            if not isinstance(value, pydantic.fields.FieldInfo)\
            or not value.extra.get('auto_assign'):
                continue
            if value.extra.get('primary_key'):
                raise TypeError(
                    f'{name}.{attname} can not be part of both the primary key '
                    'and the surrogate key.'
                )
            if namespace.get('__surrogate__') != NotImplemented:
                raise TypeError(f'{name} can not have multiple auto_assigned keys.')
            namespace['__surrogate__'] = ModelAutoAssignedIdentity(attname, value)

        new_class: 'BaseModel' = super().__new__( # type: ignore
            cls, name, bases, namespace, **params
        )
        fields: dict[str, pydantic.fields.FieldInfo] = {}
        fields.update({
            attname: field.field_info
            for attname, field in new_class.__fields__.items()
        })

        # Collect all fields that are marked as keys and create
        # ModelIdentity instances so we can use them later to
        # build queries and URLs. For now we only support one
        # key per model but natural keys also need to be supported
        # at one point.
        key_fields: list[pydantic.fields.FieldInfo] = []
        for name, field in fields.items():
            if not field.extra.get('primary_key'):
                continue
            field.extra['name'] = name
            key_fields.append(field)
        if key_fields:
            new_class.__key__ = ModelIdentity(key_fields)

        return new_class # type: ignore


class BaseModel(pydantic.BaseModel, metaclass=BaseModelMetaclass):
    __abstract__: bool = True
    __key__: ModelIdentity | NotImplementedType
    __surrogate__: ModelAutoAssignedIdentity | NotImplementedType
    __module__: str = 'cbra.types'

    def __eq__(self: T, other: T) -> bool:
        # TODO: Compare subclasses to parents if the key is the
        # same?
        return all([
            type(self) == type(other),
            self.__key__ == other.__key__ # type: ignore
        ])

    def __hash__(self) -> int: # type: ignore
        # TODO: This is implemented to support set operations,
        # but the object is mutable and thus can lead to a set
        # with multiple objects of the same identity.
        return hash(self.__key__)