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

from fastapi import FastAPI
from fastapi.routing import DecoratedCallable


from .ioc import Container
from .ioc import Requirement
from .utils import parent_signature


class Application(FastAPI):
    __module__: str = 'cbra'

    @parent_signature(FastAPI.__init__)
    def __init__(self, *args: Any, **kwargs: Any):
        self.container = Container.fromsettings()
        super().__init__(*args, **kwargs)

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

    def update_requirements(self, func: Callable[..., Any]):
        """Traverse the signature tree of the given function to find
        all :class:`Requirement` instances.
        """
        if isinstance(func, Requirement):
            func.add_to_container(self.container)
        signature = inspect.signature(func)
        for param in signature.parameters.values():
            if not isinstance(param.default, Requirement):
                continue
            param.default.add_to_container(self.container)
            if param.default.callable():
                self.update_requirements(param.default.factory) # type: ignore