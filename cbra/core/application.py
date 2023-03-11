# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import logging.config
from typing import Any
from typing import Callable

import fastapi
from fastapi import FastAPI
from fastapi.params import Depends

from cbra.types import Abortable
from .apiroute import APIRoute
from .conf import settings
from .endpointprovider import EndpointProvider
from .ioc import Requirement
from .localmessagetransport import LocalMessageTransport
from .messagepublisher import MessagePublisher
from .utils import parent_signature


class Application(FastAPI, EndpointProvider):
    __module__: str = 'cbra'
    _injectables: tuple[type, ...] = (
        Depends,
        Requirement
    )

    @parent_signature(FastAPI.__init__)
    def __init__(self, **kwargs: Any):
        EndpointProvider.__init__(self)
        handlers: dict[type, Any] = kwargs.setdefault('exception_handlers', {})
        handlers[Abortable] = self.on_aborted

        kwargs.setdefault('root_path', settings.ASGI_ROOT_PATH)
        self.inject('MessagePublisher', MessagePublisher)
        if not self.container.has('MessageTransport'):
            self.inject('MessageTransport', LocalMessageTransport)
        FastAPI.__init__(self, **kwargs)
        self.router.route_class = APIRoute
        self.add_event_handler('startup', self.setup_logging) # type: ignore

    def inject(self, name: str, value: Any) -> None:
        """Inject a value into the dependencies container."""
        self.container.inject(name, value)

    def logging_config(self):
        config = copy.deepcopy(settings.LOGGING)
        if not settings.DEBUG:
            # Remove console handler when not running in debug mode and its
            # not explicitely enabled in the settings.
            config['handlers']['console'] = {'class': 'logging.NullHandler'}
        return config

    def setup_logging(self) -> None:
        logging.config.dictConfig(self.logging_config())

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
        return self.discover_requirements(FastAPI.head, *a, **k)

    @parent_signature(FastAPI.get)
    def get(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.get, *a, **k)

    @parent_signature(FastAPI.post)
    def post(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.post, *a, **k)

    @parent_signature(FastAPI.patch)
    def patch(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.patch, *a, **k)

    @parent_signature(FastAPI.put)
    def put(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.put, *a, **k)

    @parent_signature(FastAPI.trace)
    def trace(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.trace, *a, **k)

    @parent_signature(FastAPI.options)
    def options(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.options, *a, **k)

    @parent_signature(FastAPI.delete)
    def delete(self, *a: Any, **k: Any):
        return self.discover_requirements(FastAPI.delete, *a, **k)