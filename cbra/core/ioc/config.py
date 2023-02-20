# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import cast

from unimatrix.conf import settings # type: ignore

from . import setting


__all__: list[str] = [
    'settings',
    'TRUSTED_AUTHORIZATION_SERVERS'
]

#: The list of trusted OAuth 2.x/OpenID Connect authorization
#: servers. Defaults to an empty list.
TRUSTED_AUTHORIZATION_SERVERS: list[str] = setting(
    name='TRUSTED_AUTHORIZATION_SERVERS',
    default=[]
)

settings: Any = cast(Any, settings)