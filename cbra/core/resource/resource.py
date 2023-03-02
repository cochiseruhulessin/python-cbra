# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from cbra.types import RequestPrincipal
from cbra.types import IRoutable
from ..iam import AuthorizationContextFactory
from ..sessions import RequestSession
from .iresource import IResource
from .resourcemodel import ResourceModel
from .resourcetype import ResourceType


class Resource(IResource, metaclass=ResourceType):
    __abstract__: bool = True
    __actions__: list[type[IRoutable]] = []
    __module__: str = 'cbra.core'
    context_factory: AuthorizationContextFactory = AuthorizationContextFactory.depends()
    model: type[ResourceModel]
    principal: RequestPrincipal = RequestPrincipal.depends()
    session: RequestSession = RequestSession.depends()

    def __init_subclass__(cls, model: type[ResourceModel]):
        cls.model = model

    @classmethod
    def add_to_router(cls, router: fastapi.FastAPI, **kwargs: Any) -> None:
        for action in cls.__actions__:
            kwargs.setdefault('response_model_by_alias', cls.response_model_by_alias)
            action.add_to_router(cls, router, **kwargs)

    def adapt(self, obj: Any) -> ResourceModel:
        """Adapt an object of any kind to a :class:`ResourceModel` instance.
        The default implementation simply returns the object.
        """
        return obj
    
    def parse_obj(self, obj: Any) -> Any:
        return self.model.parse_obj(obj)