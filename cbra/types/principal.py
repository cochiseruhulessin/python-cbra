# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable
from typing import Callable
from typing import Union

import pydantic

from .icredential import ICredential
from .iprincipal import IPrincipal
from .isubject import ISubject
from .nullprincipal import NullPrincipal
from .oidcprincipal import OIDCPrincipal
from .rfc9068principal import RFC9068Principal
from .sessionprincipal import SessionPrincipal


class Principal(IPrincipal, pydantic.BaseModel):
    # Note that the order is important here.
    __root__: Union[
        RFC9068Principal,
        OIDCPrincipal,
        SessionPrincipal,
        NullPrincipal
    ]

    def get_credential(self) -> ICredential | None:
        return self.__root__.get_credential()

    def has_audience(self) -> bool:
        return self.__root__.has_audience()

    def is_anonymous(self) -> bool:
        return self.__root__.is_anonymous()

    async def resolve(
        self,
        resolve: Callable[..., Awaitable[ISubject]]
    ) -> ISubject:
        return await resolve(self.__root__)

    def validate_audience(self, allow: set[str]) -> bool:
        return self.__root__.validate_audience(allow)