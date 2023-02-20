# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .httpheaderprincipal import HTTPHeaderPrincipal
from .jsonwebtokenprincipal import JSONWebTokenPrincipal


class OIDCPrincipal(HTTPHeaderPrincipal, JSONWebTokenPrincipal):
    iss: str
    sub: int | str
    exp: int
    aud: str| list[str]
    iat: int
    auth_time: int | None = None
    nonce: str | None = None
    acr: str = "0"
    amr: list[str] = []
    azp: str | None = None
    token: str

    @classmethod
    def parse_scheme(
        cls,
        values: dict[str, Any],
        scheme: str,
        value: str
    ) -> dict[str, Any]:
        if scheme != 'bearer':
            raise ValueError('this principal requires the Bearer scheme')
        values.update(cls.parse_jwt(value, accept={"application/jwt", "jwt"}))
        return values