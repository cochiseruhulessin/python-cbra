# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable

import fastapi

from .apiroute import APIRoute
from .endpointprovider import EndpointProvider
from .utils import parent_signature


class APIRouter(fastapi.APIRouter, EndpointProvider):
    __module__: str = 'cbra.core'

    @parent_signature(fastapi.APIRouter.__init__)
    def __init__(self, *args: Any, **kwargs: Any):
        kwargs.setdefault('route_class', APIRoute)
        super().__init__(*args, **kwargs)

    @parent_signature(fastapi.APIRouter.add_api_route)
    def add_api_route(
        self,
        endpoint: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.update_requirements(endpoint)
        return super().add_api_route(endpoint=endpoint, *args, **kwargs)

    def add_to_router(
        self,
        router: Any,
        *args: Any,
        **kwargs: Any
    ) -> None:
        router.include_router(self)

    @parent_signature(fastapi.APIRouter.head)
    def head(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.head, *a, **k)

    @parent_signature(fastapi.APIRouter.get)
    def get(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.get, *a, **k)

    @parent_signature(fastapi.APIRouter.post)
    def post(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.post, *a, **k)

    @parent_signature(fastapi.APIRouter.patch)
    def patch(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.patch, *a, **k)

    @parent_signature(fastapi.APIRouter.put)
    def put(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.put, *a, **k)

    @parent_signature(fastapi.APIRouter.trace)
    def trace(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.trace, *a, **k)

    @parent_signature(fastapi.APIRouter.options)
    def options(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.options, *a, **k)

    @parent_signature(fastapi.APIRouter.delete)
    def delete(self, *a: Any, **k: Any):
        return self.discover_requirements(fastapi.APIRouter.delete, *a, **k)