# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import collections
import inspect
import uuid
from typing import get_args
from typing import get_origin
from typing import Awaitable
from typing import Any
from typing import Callable
from typing import Generic
from typing import TypeVar
from typing import Union
from inspect import Parameter

import fastapi
import fastapi.params
import pydantic

from cbra.types import Abortable
from cbra.types import IEndpoint
from cbra.types import IntegerPathParameter
from cbra.types import MutableSignature
from cbra.types import PathParameter
from cbra.types import StringPathParameter
from cbra.types import UUIDPathParameter


E = TypeVar('E', bound='IEndpoint')
T = TypeVar('T', bound='RequestHandler[Any]')


class RequestHandler(Generic[E]):
    __module__: str = 'cbra'
    _is_coroutine = asyncio.coroutines._is_coroutine # type: ignore
    _annotations: tuple[type, ...] = (
        fastapi.Request,
        fastapi.Response,
    )
    _class: type[E] | None
    _class_params: set[str]
    _dependencies: dict[str, Parameter] = {}
    _func: Callable[..., Awaitable[Any] | Any]
    _handler_params: set[str]
    _init_params: set[str]
    _injectables: tuple[type, ...] = (
        fastapi.params.Body,
        fastapi.params.Depends,
        fastapi.params.Param,
    )
    _method: str
    _path_types: dict[type, type[PathParameter]] = {
        int: IntegerPathParameter,
        str: StringPathParameter,
        uuid.UUID: UUIDPathParameter
    }
    _signature: inspect.Signature | None
    include_in_schema: bool = True
    response_model_by_alias: bool = False
    status_code: int = 200

    @property
    def attname(self) -> str:
        return str.lower(self._method)

    @property
    def endpoint(self) -> type[E]:
        assert self._class is not None
        return self._class

    @property
    def method(self) -> str:
        return str.upper(self._method)

    @property
    def __signature__(self) -> inspect.Signature:
        assert self._signature is not None
        return self._signature

    @property # type: ignore
    def __doc__(self) -> str | None:
        return self._func.__doc__

    def __init__(
        self,
        name: str,
        method: str,
        func: Callable[..., Awaitable[Any] | Any],
        include_in_schema: bool | None = None,
        response_model_by_alias: bool = False
    ):
        self._endpoint_name = name
        self._class = None
        self._class_args = []
        self._class_params = set()
        self._dependencies = {}
        self._handler_params = set()
        self._handler_sig = MutableSignature.fromfunction(func)
        self._init_params = set()
        self._method = method
        self._func = func
        self._func, self._handler_sig = self.validate_handler(self._func, self._handler_sig)
        if include_in_schema is not None:
            self.include_in_schema = include_in_schema
        self.response_model_by_alias = response_model_by_alias
        # Check if the asyncio.iscoroutinefunction() call returns
        # True for this object, since it depends on a private
        # symbol.
        assert asyncio.iscoroutinefunction(self) # nosec

    def clone(self: T) -> T:
        return type(self)(
            self._endpoint_name,
            self.method,
            self._func,
            self.include_in_schema
        )

    def annotate_path(self, cls: Any) -> type[PathParameter]:
        return self._path_types[cls]

    def get_return_annotation(self) -> Any:
        return self._handler_sig.return_annotation

    def is_injectable(self, cls: Any) -> bool:
        """Return a boolean indicating if the class is injectable."""
        cls = get_origin(cls) or cls
        return any([
            inspect.isclass(cls) and issubclass(cls, self._annotations),
            cls in self._annotations
        ])

    def validate_handler(
        self,
        func: Callable[..., Awaitable[Any] | Any],
        signature: MutableSignature
    ) -> tuple[Callable[..., Awaitable[Any] | Any], MutableSignature]:
        return func, signature

    def add_to_class(self, cls: type[IEndpoint]) -> None:
        """Construct an entrypoint for the router and add it to the
        endpoint class.
        """
        self._class = cls # type: ignore
        self._class_sig = MutableSignature.fromfunction(cls)

        # Collect all dependencies and ensure that there are no clashing
        # attribute or parameter names.
        dependencies = self._dependencies
        annotations: dict[str, type] = getattr(cls, '__annotations__') or {}

        # Begin with inspecting the annotations, these might contain automatically
        # injectable objects such as fastapi.Request.
        for attname, annotation in annotations.items():
            if hasattr(cls, attname):
                # Is a dependency or has a default, see below.
                continue
            if not self.can_inject(annotation, 'class'):
                continue
            dependencies[attname] = Parameter(
                kind=Parameter.POSITIONAL_ONLY,
                name=attname,
                annotation=annotation
            )
            self._class_params.add(attname)

        for attname, value in inspect.getmembers(cls):
            if not self.can_inject(value, 'class'):
                continue
            dependencies[attname] = Parameter(
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                name=attname,
                annotation=annotations.get(attname),
                default=value
            )
            self._class_params.add(attname)

        # If the constructor has named parameters, then the __init__
        # was overridden and also might contain dependencies.
        for param in self._class_sig.named:
            if not self.can_inject(param, 'init'):
                raise TypeError("Constructor arguments must be injectable.")
            if param.name in {'request', 'response'}:
                raise ValueError(f'Can not inject {param.name}')
            if param.name in dependencies:
                raise TypeError(
                    f"{cls.__name__} dependency '{param.name}' conflicts "
                    f"with dependency {cls.__name__}.{param.name}."
                )
            dependencies[param.name] = param
            self._init_params.add(param.name)

        # Finally, get the dependencies from the request handler.
        for param in self._handler_sig.named:
            if param.name == 'self' or not self.can_inject(param, 'handler'):
                continue
            if param.name in {'request', 'response'}:
                raise ValueError(f'Can not inject {param.name}')
            if param.name in dependencies:
                raise TypeError(
                    f"{cls.__name__}.{self.attname} dependency "
                    f"'{param.name}' conflicts with {cls.__name__}.{param.name} "
                    "or a constructor argument."
                )

            annotation = param.annotation
            default = param.default

            # Wrap the annotation if it is an injectable path parameter,
            # because we don't want to return 422 like FastAPI does but
            # a proper 404.
            if annotation in self._path_types\
            and not isinstance(default, self._injectables):
                annotation = self.annotate_path(annotation)

            dependencies[param.name] = Parameter(
                kind=(
                    Parameter.POSITIONAL_OR_KEYWORD
                    if param.default != Parameter.empty
                    else Parameter.POSITIONAL_ONLY
                ),
                name=param.name,
                annotation=annotation,
                default=default
            )
            self._handler_params.add(param.name)

        # Sort the parameters so that the order is correct. Also force add
        # some dependencies.
        dependencies['request'] = Parameter(
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            name='request',
            annotation=fastapi.Request
        )
        dependencies['response'] = Parameter(
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            name='response',
            annotation=fastapi.Response
        )
        self._class_params.add('request')
        self._class_params.add('response')

        parameters = list(dependencies.values())
        for i, p in enumerate(parameters):
            parameters[i] = self.preprocess_parameter(p) or p
        parameters, return_annotation = self.preprocess_signature(
            parameters={p.name: p for p in parameters},
            return_annotation=self.get_return_annotation()
        )
        parameters = [
            *[
                p for p in parameters
                if p.kind == Parameter.POSITIONAL_ONLY
                and p.default == Parameter.empty
            ],
            *[
                p for p in parameters
                if p.kind == Parameter.POSITIONAL_ONLY
                and p.default != Parameter.empty
            ],
            *[
                p for p in parameters
                if p.kind == Parameter.POSITIONAL_OR_KEYWORD
                and p.default == Parameter.empty
            ],
            *[
                p for p in parameters
                if p.kind == Parameter.POSITIONAL_OR_KEYWORD
                and p.default != Parameter.empty
            ],
            *[p for p in parameters if p.kind == Parameter.KEYWORD_ONLY],
        ]

        sig = inspect.signature(self.__call__)
        self._dependencies = collections.OrderedDict([
            (param.name, param) for param in parameters
        ])
        self._signature = sig.replace(
            parameters=parameters,
            return_annotation=return_annotation
        )

    def add_to_router(
        self,
        cls: IEndpoint,
        router: fastapi.APIRouter,
        **kwargs: Any
    ) -> None:
        assert self._class is not None
        if self.method == 'OPTIONS':
            kwargs.update({'response_model': None, 'status_code': 200})
        if self._handler_sig.return_annotation == None:
            # Ensure that a proper response code is presented to
            # FastAPI if the handler does not return anything.
            kwargs.update({
                'response_model': None,
                'status_code': 204
            })
        kwargs.setdefault('name', cls.name)
        kwargs.setdefault('response_model_by_alias', cls.response_model_by_alias)
        kwargs.update(getattr(self._func, 'params', {}))
        router.add_api_route(
            endpoint=self,
            methods=[self.method],
            include_in_schema=self._class.include_in_schema\
                and self.include_in_schema,
            **kwargs,
        )

    def can_inject(self, p: Parameter | Any, where: str) -> bool:
        return any([
            isinstance(p, Parameter)\
                and inspect.isclass(p.annotation) and self.is_injectable(p.annotation),
            isinstance(p, Parameter)\
                and isinstance(p.default, self._injectables),
            isinstance(p, Parameter) and (where=='handler')\
                and p.annotation in (self._path_types),\
            isinstance(p, Parameter) and (where=='handler')\
                and self.is_pydantic_union(p.annotation),
            isinstance(p, Parameter) and (where=='handler')\
                and get_origin(p.annotation) is None\
                and inspect.isclass(p.annotation)\
                and issubclass(p.annotation, pydantic.BaseModel),
            isinstance(p, Parameter) and (where=='handler')\
                and get_origin(p.annotation) == dict,
            not isinstance(p, Parameter)\
                and isinstance(p, self._injectables),
            not isinstance(p, Parameter) and self.is_injectable(p)
        ])

    def is_pydantic_union(self, obj: Any):
        origin = get_origin(obj)
        if origin != Union:
            return False
        return all([
            isinstance(x, pydantic.main.ModelMetaclass)
            for x in get_args(obj)
        ])

    def preprocess_parameter(self, p: Parameter) -> Parameter | None:
        """Hook to modify a parameter just before it is added to the
        new signature. It is expected to return a modified
        :class:`inspect.Parameter` instance.
        """
        return p

    def preprocess_signature(
        self,
        parameters: dict[str, Parameter],
        return_annotation: Any
    ) -> tuple[list[Parameter], Any]:
        return list(parameters.values()), return_annotation

    async def preprocess_value(self, name: str, value: Any) -> Any:
        return value

    async def process_response(
        self,
        endpoint: IEndpoint,
        response: fastapi.Response | pydantic.BaseModel | None
    ) -> fastapi.Response:
        if response is None:
            response = fastapi.Response(status_code=204)
        elif isinstance(response, pydantic.BaseModel):
            response = fastapi.responses.Response(
                headers={'Content-Type': "application/json"},
                status_code=self.status_code,
                content=response.json(
                    by_alias=endpoint.response_model_by_alias,
                    indent=2,
                )
            )
        elif isinstance(response, dict):
            response = fastapi.responses.JSONResponse(
                status_code=self.status_code,
                content=response
            )
        assert isinstance(response, fastapi.Response), type(response) # nosec
        response.headers.update(endpoint.get_success_headers(response))
        return response

    async def __call__(self, **params: Any) -> Any:
        try:
            return await self._run_handler(**params)
        except Abortable as exc:
            return await exc.as_response()

    async def _run_handler(self, **params: Any) -> Any:
        # Construct the init arguments, instance attributes and handler
        # arguments from the known parameters.
        assert self._class is not None
        attrs: dict[str, Any] = {}
        init: dict[str, Any] = {}
        kwargs: dict[str, Any] = {}
        for param in self._dependencies.values():
            value = await self.preprocess_value(param.name, params.pop(param.name))

            # PathParameter instances expose a clean() method
            # that immetialy cause the endpoint to return 404
            # on validation failure.
            if inspect.isclass(param.annotation)\
            and issubclass(param.annotation, PathParameter):
                value = param.annotation.clean(value)

            if param.name in self._init_params:
                init[param.name] = value
            elif param.name in self._class_params:
                attrs[param.name] = value
            elif param.name in self._handler_params:
                kwargs[param.name] = value

        if params:
            raise TypeError("Received unknown arguments.")

        # Initialize the endpoint and set its attributes, proceed
        # to invoke the handler.
        endpoint: IEndpoint = self._class(**init)
        endpoint.__dict__.update(attrs)
        response = await self.process_response(
            endpoint,
            await endpoint.run_handler(self._func, **kwargs)
        )

        # Persist the session only if there is a successful response.
        if (200 <= response.status_code < 400) \
        and endpoint.session.is_dirty():
            await endpoint.session.add_to_response(response)

        # Copy the headers from the endpoint response.
        response.raw_headers = [
            *response.raw_headers,
            *endpoint.response.raw_headers
        ]

        return response