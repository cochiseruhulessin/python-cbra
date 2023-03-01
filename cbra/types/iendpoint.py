# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import logging
from datetime import datetime
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Literal
from typing import TypeVar

import fastapi

from .abortable import Abortable
from .iauthorizationcontextfactory import IAuthorizationContextFactory
from .irequestprincipal import IRequestPrincipal
from .iroutable import IRoutable
from .isessionmanager import ISessionManager
from .forbidden import Forbidden
from .notauthorized import NotAuthorized


T = TypeVar('T', bound='IEndpoint')


class IEndpoint:
    __module__: str = 'cbra.types'
    allowed_http_methods: list[str]
    context_factory: IAuthorizationContextFactory
    handlers: list[IRoutable]
    include_in_schema: bool = True
    name: str | None = None
    logger: logging.Logger = logging.getLogger('cbra.endpoint')
    response_model_by_alias: bool = False
    session: ISessionManager[Any]
    with_options: bool = True

    #: The set of permissions supported by this endpoint. These must be
    #: defined beforehand to limit the number of calls to remote IAM
    #: systems.
    permissions: set[str]

    #: The list of subjects that may access this endpoint. Override this
    #: property if an endpoint needs to hardcode the allowed subjects
    #: that may invoke it, for example when expecting a request from
    #: Google using a priorly known service account.
    allowed_subjects: set[str] = set()

    #: The set of trusted authorization servers. This will override the
    #: :attr:`cbra.core.conf.settings.TRUSTED_AUTHORIZATION_SERVERS`
    #: setting.
    trusted_providers: set[str] = set()

    principal: IRequestPrincipal
    request: fastapi.Request
    response: fastapi.Response
    router: fastapi.APIRouter

    #: Indicates if all requests to the endpoint must be authenticated.
    require_authentication: bool = False
    status_code: int = 200
    summary: str | None = None
    tags: list[str] = []

    @staticmethod
    def require_permission(name: str) -> Callable[..., Any]:
        """Decorate a method on an :class:`~cbra.types.IEndpoint` implementation
        to require the given permission. If the request does not have permission
        `name`, then :class:`~cbra.types.Forbidden` is raised.
        """
        def decorator_factory(
            func: Callable[..., Any]
        ) -> Callable[['IEndpoint'], Awaitable[Any]]:
            @functools.wraps(func)
            async def f(self: 'IEndpoint', *args: Any, **kwargs: Any) -> Any:
                if not await self.is_authorized(name):
                    raise Forbidden
                return await func(self, *args, **kwargs)
            return f
        return decorator_factory

    @classmethod
    def configure(cls: type[T], overrides: dict[str, Any]) -> type[T]:
        return type(cls.__name__, (cls,), overrides) # type: ignore

    async def get_allowed_subjects(self) -> set[str]:
        """Return the set of allowed subjects that may access this resource.
        By default, returns :attr:`allowed_subjects`.
        """
        return self.allowed_subjects

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
        try:
            await self.authenticate()
            if self.require_authentication and not self.ctx.is_authenticated():
                raise NotAuthorized
            return await func(self, *args, **kwargs)
        except Abortable as exc:
            return await exc.as_response()

    async def authenticate(self) -> None:
        self.ctx = await self.context_factory.authenticate(
            request=self.request,
            principal=self.principal,
            providers=self.trusted_providers,
            subjects=await self.get_allowed_subjects()
        )

    async def is_authorized(self, name: str) -> bool:
        """Return a boolean if the given authorization context has a
        certain permission.
        """
        await self.ctx.authorize()
        return self.has_permission(name)

    def has_permission(self, name: str) -> bool:
        """Return a boolean if the request has the given permission."""
        return self.ctx.has_permission(name)

    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: int | None = None,
        expires: datetime | str| int | None = None,
        path: str = "/",
        domain: str | None = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Literal["lax", "strict", "none"] | None = "lax",
    ) -> None:
        self.response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            samesite=samesite
        )

    def delete_cookie(self, key: str, path: str = "/") -> None:
        return self.set_cookie(key, expires=0, max_age=0, path=path)