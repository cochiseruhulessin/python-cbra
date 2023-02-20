# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any
from typing import Callable

import fastapi
from fastapi import FastAPI
from fastapi.routing import DecoratedCallable
from fastapi.params import Depends

from cbra.types import Abortable
from .endpoint import Endpoint
from .resource import Resource
from .ioc import Container
from .ioc import Requirement
from .utils import parent_signature


class Application(FastAPI):
    __module__: str = 'cbra'
    _injectables: tuple[type, ...] = (
        Depends,
        Requirement
    )

    @parent_signature(FastAPI.__init__)
    def __init__(self, *args: Any, **kwargs: Any):
        self.container = Container.fromsettings()

        handlers: dict[type, Any] = kwargs.setdefault('exception_handlers', {})
        handlers[Abortable] = self.on_aborted

        super().__init__(*args, **kwargs)

    def add(
        self,
        routable: type[Endpoint | Resource],
        *args: Any, **kwargs: Any
    ) -> None:
        routable.add_to_router(self, *args, **kwargs)

    def inject(self, name: str, value: Any) -> None:
        """Inject a value into the dependencies container."""
        self.container.inject(name, value)

    async def on_aborted(
        self,
        request: fastapi.Request,
        exc: Abortable
    ) -> fastapi.Response:
        return await exc.as_response()

    @parent_signature(FastAPI.add_api_route)
    def add_api_route(
        self,
        endpoint: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.update_requirements(endpoint)
        return super().add_api_route(endpoint=endpoint, *args, **kwargs)

    @parent_signature(FastAPI.head)
    def head(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.get)
    def get(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.post)
    def post(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.patch)
    def patch(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.put)
    def put(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.trace)
    def trace(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.options)
    def options(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.delete)
    def delete(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    def discover_requirements(
        self,
        decorator_factory: Callable[..., DecoratedCallable],
        *args: Any,
        **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.update_requirements(func)
            return decorator_factory(self, *args, *kwargs)(func)
        return decorator

    def update_requirements(self, func: Callable[..., Any] | Depends | Any) -> None:
        """Traverse the signature tree of the given function to find
        all :class:`Requirement` instances.
        """
        # TODO: this will completely mess up if multiple Application instances
        # are spawned.
        if not callable(func): return None
        if isinstance(func, Depends):
            return self.update_requirements(func.dependency)
        if isinstance(func, Requirement):
            func.add_to_container(self.container)
        signature = inspect.signature(func) # type: ignore
        for param in signature.parameters.values():
            if not isinstance(param.default, self._injectables):
                continue
            if isinstance(param.default, Requirement):
                param.default.add_to_container(self.container)
                if param.default.callable():
                    self.update_requirements(param.default.factory) # type: ignore
                continue

            if isinstance(param.default, Depends):
                injectable = param.default.dependency
                if injectable is None:
                    # Was declared as f(dependency: Callable = fastapi.Depends())
                    injectable = param.annotation
                self.update_requirements(injectable)