# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from .iprincipal import IPrincipal
from .nullprincipal import NullPrincipal
from .oidcprincipal import OIDCPrincipal
from .rfc9068principal import RFC9068Principal


class Principal(IPrincipal, pydantic.BaseModel):
    __root__: RFC9068Principal | OIDCPrincipal | NullPrincipal

    def is_anonymous(self) -> bool:
        return self.__root__.is_anonymous()