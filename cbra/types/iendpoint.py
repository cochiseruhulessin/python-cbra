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

from .iauthorizationcontextfactory import IAuthorizationContextFactory
from .iprincipal import IPrincipal
from .iroutable import IRoutable
from .notauthorized import NotAuthorized


class IEndpoint:
    __module__: str = 'cbra.types'
    allowed_http_methods: list[str]
    context_factory: IAuthorizationContextFactory
    handlers: list[IRoutable]
    include_in_schema: bool = True
    principal: IPrincipal
    request: fastapi.Request
    response: fastapi.Response
    router: fastapi.APIRouter

    #: Indicates if all requests to the endpoint must be authenticated.
    require_authentication: bool = False

    def get_success_headers(self, data: Any) -> dict[str, Any]:
        """Return a mapping holding the headers to add on a successful
        request based on the return value of the request handler.
        """
        return {}

    async def run_handler(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ):
        self.ctx = await self.context_factory.setup(self.request, self.principal)
        if self.require_authentication and not self.ctx.is_authenticated():
            raise NotAuthorized
        return await func(self, *args, **kwargs)