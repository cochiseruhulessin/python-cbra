# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .icredential import ICredential
from .httpheaderprincipal import HTTPHeaderPrincipal
from .jsonwebtoken import JSONWebToken
from .jsonwebtokenprincipal import JSONWebTokenPrincipal


class RFC9068RequestPrincipal(HTTPHeaderPrincipal, JSONWebTokenPrincipal):
    iss: str
    aud: str| list[str]
    exp: int
    sub: str
    client_id: str
    iat: int
    jti: str
    auth_time: int | None = None
    acr: str | None = None
    amr: list[str] | None = []
    scope: str | None = None

    @classmethod
    def parse_scheme(
        cls,
        values: dict[str, Any],
        scheme: str,
        value: str
    ) -> dict[str, Any]:
        if scheme != 'bearer':
            raise ValueError('this principal requires the Bearer scheme')
        values.update(cls.parse_jwt(value, accept={"application/at+jwt", "at+jwt"}))
        return values

    def get_audience(self) -> set[str]:
        audience = self.aud
        if isinstance(audience, str):
            audience = {audience}
        return set(audience)

    def get_credential(self) -> ICredential | None:
        return JSONWebToken(self.token)

    def has_audience(self) -> bool:
        return True

    def validate_audience(self, allow: set[str]) -> bool:
        aud = self.aud
        if isinstance(aud, str):
            aud = {aud}
        return bool(set(aud) & allow)