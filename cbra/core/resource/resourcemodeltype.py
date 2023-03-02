# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import types
from typing import Any
from typing import Literal
from typing import Union
from typing import get_args
from typing import get_origin

import pydantic
import pydantic.main
import pydantic.schema

from .resourceidentifier import ResourceIdentifier
from .resourcelist import ResourceList


class ResourceModelType(pydantic.main.ModelMetaclass):

    def __new__( # type: ignore
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ):
        annotations: dict[str, type] = namespace.get('__annotations__') or {}
        is_abstract = namespace.pop('__abstract__', False)
        if not is_abstract:
            # Collect readonly fields to create the CreateResourceRequest
            # ReplaceResourceRequest and UpdateResourceRequest models.
            create_fields: list[tuple[str, type, pydantic.main.FieldInfo | None]] = []
            key_fields: list[tuple[str, type, pydantic.main.FieldInfo]] = []
            update_fields: list[tuple[str, type, pydantic.main.FieldInfo | None]] = []
            response_fields: list[tuple[str, type, pydantic.main.FieldInfo | None]] = []
            for attname, class_ in annotations.items():
                field = namespace.get(attname)
                if isinstance(field, pydantic.main.FieldInfo):
                    response_fields.append((attname, class_, cls.get_field(field, 'response')))
                    if field.extra.get('primary_key'):
                        key_fields.append((attname, class_, field))
                    continue
                create_fields.append((attname, class_, cls.get_field(field, 'create')))
                update_fields.append((attname, class_, cls.get_field(field, 'update')))
                response_fields.append((attname, class_, cls.get_field(field, 'response')))

            PartialModel = type('Partial{name}Request', (pydantic.BaseModel,), {
                '__annotations__': {attname: class_ for attname, class_, _ in create_fields},
                **{name: field for name, _, field in create_fields if field is not None},
            })
            UpdateResourceRequest = type(f'Update{name}Request', (pydantic.BaseModel,), {
                '__annotations__': {attname: cls.allow_empty(class_) for attname, class_, _ in update_fields},
                **{name: field for name, _, field in update_fields if field is not None},
            })
            ResponseModel = type(name, (pydantic.BaseModel,), {
                '__annotations__': {attname: cls.ensure_required(field, class_) for attname, class_, field in response_fields},
                **{name: field for name, _, field in response_fields if name in namespace},
            })
            namespace.update({
                '__create_model__': type(f'Create{name}Request', (PartialModel,), {}),
                '__update_model__': UpdateResourceRequest,
                '__replace_model__': type(f'Replace{name}Request', (PartialModel,), {}),
                '__response_model__': ResponseModel,
                '__list_model__': type(f'{name}List', (ResourceList,), {
                    '__annotations__': {
                        'kind': Literal[f'{name}List'], # type: ignore
                        'items': list[ResponseModel]
                    },
                    'items': pydantic.Field(
                        default=...,
                        title=f'{name} array',
                        description=f'Items in the list of **{name}** resources.'
                    ),
                    'kind': pydantic.Field(
                        default=...,
                        required=[name]
                    )
                })
            })
            if key_fields:
                namespace.update({
                    '__key_model__': type(f'{name}Identifier', (ResourceIdentifier,), {
                        '__annotations__': {attname: cls.ensure_required(field, class_) for attname, class_, field in key_fields},
                        **{name: field for name, _, field in key_fields if name in namespace},
                    })
                })

        return super().__new__(cls, name, bases, namespace, **params) # type: ignore

    @staticmethod
    def allow_empty(value: Any) -> Any:
        return value | None

    @staticmethod
    def ensure_required(field: pydantic.fields.FieldInfo | None, value: Any) -> Any:
        origin = get_origin(value)
        if origin == types.UnionType and field and field.extra.get('read_only'):
            args: list[Any] = [x for x in get_args(value) if x != types.NoneType]
            if not args:
                raise TypeError("Field can not only contain None.")
            value = args[0]
            if len(args) > 1:
                value = Union[tuple(args)] # type: ignore
        return value

    @staticmethod
    def get_field(
        field: pydantic.main.FieldInfo | None,
        action: str
    ) -> pydantic.main.FieldInfo | None:
        field = copy.deepcopy(field)
        if isinstance(field, pydantic.main.FieldInfo) and field.extra.get('read_only'):
            if action not in {'response', 'key'}:
                return
            field.update_from_config({
                'default': ...,
            })
        elif isinstance(field, pydantic.main.FieldInfo) and action == 'update':
            field.update_from_config({'default': None})
        return field

