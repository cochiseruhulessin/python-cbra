# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.types import ICredentialVerifier
from cbra.types import IRequestPrincipal
from cbra.types import ISubject


class Subject(ISubject):
    sub: str
    principal: IRequestPrincipal
    authenticated: bool = False

    def __init__(
        self,
        *,
        id: str,
        email: str | None,
        principal: IRequestPrincipal
    ):
        self.email = email
        self.sub = id
        self.principal = principal

    async def authenticate(
        self,
        verifier: ICredentialVerifier[Any],
        providers: set[str] | None = None
    ) -> None:
        self.authenticated = await verifier.verify(
            self.principal,
            self.principal.get_credential(),
            providers=providers
        )

    def is_authenticated(self) -> bool:
        return self.authenticated

    def __repr__(self) -> str:
        return f'Subject(id={self.sub})'