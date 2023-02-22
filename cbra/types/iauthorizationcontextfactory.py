# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Awaitable

import fastapi

from .iauthorizationcontext import IAuthorizationContext
from .irequestprincipal import IRequestPrincipal


class IAuthorizationContextFactory:
    """Setup an authorization context for a request."""
    __module__: str = 'cbra.types'

    async def authenticate(
        self,
        request: fastapi.Request,
        principal: IRequestPrincipal,
        providers: set[str] | None = None,
        subjects: set[str] | Awaitable[set[str]] | None  = None,
        claims: dict[str, Any] | None = None
    ) -> IAuthorizationContext:
        raise NotImplementedError

    def validate_audience(self, principal: IRequestPrincipal, allow: set[str]) -> None:
        raise NotImplementedError