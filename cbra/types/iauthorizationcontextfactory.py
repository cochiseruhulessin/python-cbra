# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from .iauthorizationcontext import IAuthorizationContext
from .iprincipal import IPrincipal


class IAuthorizationContextFactory:
    """Setup an authorization context for a request."""
    __module__: str = 'cbra.types'

    async def authenticate(
        self,
        request: fastapi.Request,
        principal: IPrincipal,
        providers: set[str] | None = None
    ) -> IAuthorizationContext:
        raise NotImplementedError

    def validate_audience(self, principal: IPrincipal, allow: set[str]) -> None:
        raise NotImplementedError