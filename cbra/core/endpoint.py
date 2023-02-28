# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import TypeVar

import fastapi

from cbra.types import IAuthorizationContext
from cbra.types import IEndpoint
from cbra.types import RequestPrincipal
from .iam import AuthorizationContextFactory
from .endpointtype import EndpointType
from .sessions import RequestSession


T = TypeVar('T')


class Endpoint(IEndpoint, metaclass=EndpointType):
    __abstract__: bool = True
    __module__: str = 'cbra'
    allowed_http_methods: list[str]
    include_in_schema: bool = True
    principal: RequestPrincipal = RequestPrincipal.depends()
    ctx: IAuthorizationContext
    context_factory: AuthorizationContextFactory = AuthorizationContextFactory.depends()
    session: RequestSession = RequestSession.depends()
    timestamp: datetime

    def __init__(self, **kwargs: Any):
        """Constructor. Called in the router; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.timestamp = datetime.now(timezone.utc)

    @classmethod
    def add_to_router(cls, router: fastapi.FastAPI, **kwargs: Any) -> None:
        kwargs.setdefault('path', '/')
        kwargs.setdefault('response_model_by_alias', cls.response_model_by_alias)
        kwargs.setdefault('status_code', cls.status_code)
        kwargs.setdefault('summary', cls.summary)
        kwargs.setdefault('tags', cls.tags)
        for handler in cls.handlers:
            handler.add_to_router(cls, router, **kwargs)