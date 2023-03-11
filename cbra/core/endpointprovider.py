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
from typing import Union
from typing import TypeVar

import aorta
import fastapi
from fastapi.routing import DecoratedCallable
from fastapi.params import Depends

from .endpoint import Endpoint
from .ioc import Container
from .ioc import Requirement
from .resource import Resource


T = TypeVar('T', bound='EndpointProvider')


class EndpointProvider:
    container: Container
    _injectables: tuple[type, ...] = (
        Depends,
        Requirement
    )

    def __init__(self):
        self.container = Container.fromsettings()

    def add(
        self: T,
        routable: Union[
            type[Endpoint | Resource],
            type[aorta.EventListener |aorta.CommandHandler],
            type[fastapi.APIRouter],
            fastapi.APIRouter,
            T,
            Any
        ],
        *args: Any, **kwargs: Any
    ) -> None:
        if hasattr(routable, 'add_to_router'):
            routable.add_to_router(self, *args, **kwargs) # type: ignore
        elif inspect.isclass(routable) and issubclass(routable, (Endpoint, Resource)):
            routable.add_to_router(self, *args, **kwargs) # type: ignore
        elif inspect.isclass(routable) and issubclass(routable, aorta.MessageHandler):
            # Ensure that all members are injected in the container.
            for _, member in inspect.getmembers(routable):
                if not isinstance(member, (Depends, Requirement)):
                    continue
                self.update_requirements(member)
            aorta.register(routable)
        elif inspect.isclass(routable) and issubclass(routable, type(self)):
            self.add(routable(), *args, **kwargs)
        elif inspect.isclass(routable) and issubclass(routable, fastapi.APIRouter):
            self.add(routable(), *args, **kwargs)
        elif isinstance(routable, fastapi.APIRouter):
            self.include_router(routable, *args, **kwargs) # type: ignore
        else:
            raise NotImplementedError

    def discover_requirements(
        self,
        decorator_factory: Callable[..., DecoratedCallable],
        *args: Any,
        **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self.update_requirements(func)
            return decorator_factory(self, *args, **kwargs)(func)
        return decorator

    def update_requirements(self, func: Callable[..., Any] | Depends | Any) -> None:
        """Traverse the signature tree of the given function to find
        all :class:`Requirement` instances.
        """
        # TODO: this will completely mess up if multiple Application instances
        # are spawned.
        if not callable(func): return None
        if isinstance(func, Requirement):
            func.add_to_container(self.container)
        elif isinstance(func, Depends):
            return self.update_requirements(func.dependency)
        try:
            signature = inspect.signature(func) # type: ignore
        except ValueError:
            # No signature to inspect.
            return None
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