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
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi
import pydantic

from ..requesthandler import RequestHandler
from ..types import MutableSignature
from .iresource import IResource


T = TypeVar('T', bound='ResourceAction')


class ResourceAction(RequestHandler[IResource]): # type: ignore
    action: str
    name_template: str
    response_description: str = 'Successful response'
    status_code: int = 200

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        raise NotImplementedError

    @property
    def article(self) -> str:
        article = 'a'
        if self.name[0] in {'a', 'e', 'i', 'o', 'u'}:
            article = 'an'
        return article

    @property
    def name(self) -> str:
        return self.endpoint.model.__name__

    @property
    def response_model(self) -> type[pydantic.BaseModel]:
        return self.endpoint.model.__response_model__

    @property
    def path_parameter_name(self) -> str:
        return f'{self.endpoint.resource_name.lower()}_id'

    @property
    def summary(self) -> str:
        # TODO
        return self.name_template.format(
            article=self.article,
            name=self.name,
            pluralname=self.endpoint.verbose_name_plural
        )

    def add_to_router(self, router: fastapi.APIRouter, **kwargs: Any) -> None:
        kwargs.setdefault('status_code', self.status_code)
        kwargs.setdefault('summary', self.summary)
        tags: list[str] = kwargs.setdefault('tags', [])
        tags.append(self.name)
        kwargs.update({
            'path': self.get_url_pattern(kwargs.get('path')),
            'response_description': self.response_description.format(
                name=self.name,
                pluralname=self.endpoint.verbose_name_plural,
                article=self.article
            )
        })
        kwargs['responses'] = self.get_openapi_responses(kwargs.get('responses') or {})
        return super().add_to_router(router, **kwargs)

    def can_write(self) -> bool:
        raise NotImplementedError

    def get_openapi_responses(
        self,
        responses: dict[int | str, Any]
    ) -> dict[int | str, Any]:
        return responses

    def get_url_pattern(self, prefix: str | None) -> str:
        path: str | None = prefix
        if path is None:
            path = f'/{self.endpoint.path_name}'
        else:
            path = f"{str.lstrip(path, '/')}/{self.endpoint.path_name}"
        return path

    def get_write_model(self) -> type[pydantic.BaseModel]:
        raise NotImplementedError

    def is_detail(self) -> bool:
        raise NotImplementedError

    def parse_resource(self, resource: pydantic.BaseModel) -> pydantic.BaseModel:
        raise NotImplementedError

    def preprocess_parameter(self, p: Parameter) -> Parameter | None:
        """Hook to modify a parameter just before it is added to the
        new signature.
        """
        if self.can_write() and p.name == 'resource':
            return Parameter(
                kind=p.kind,
                name=p.name,
                annotation=self.get_write_model(),
                default=p.default
            )

    def validate_handler(
        self,
        func: Callable[..., Awaitable[Any] | Any],
        signature: MutableSignature
    ) -> tuple[Callable[..., Awaitable[Any] | Any], MutableSignature]:
        if not signature.has_param('resource') and self.can_write():
            raise TypeError(
                f"{self._endpoint_name}.{self.action} must accept "
                "the 'resource' positional argument."
            )
        return super().validate_handler(func, signature)

    async def preprocess_value(self, name: str, value: Any) -> Any:
        if name == 'resource':
            value = self.parse_resource(value)
        return await super().preprocess_value(name, value)