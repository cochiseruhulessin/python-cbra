# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import overload
from typing import Any
from typing import Protocol

from canonical import EmailAddress
from headless.ext.oauth2.models import OIDCToken
from headless.ext.oauth2.models import SubjectIdentifier

from .subject import Subject
from .principaltype import PrincipalType


class IUserOnboardingService(Protocol):

    @overload
    async def can_use(
        self,
        subject: Subject,
        principals: list[EmailAddress | SubjectIdentifier]
    ) -> bool: ...

    @overload
    async def can_use(self, token: OIDCToken) -> bool: ...

    @overload
    async def get(self, oidc: OIDCToken) -> Subject | None: ...

    @overload
    async def get(self, uid: int) -> Subject | None: ...

    async def update(
        self,
        subject: Subject,
        iss: str,
        principals: list[Any],
        trust: bool
    ) -> None: ...

    async def update_oidc(
        self,
        subject: Subject,
        oidc: OIDCToken
    ) -> None: ...

    def initialize(self) -> Subject: ...
    async def destroy(self, uid: int) -> None: ...
    async def email(self, issuer: str, email: EmailAddress) -> tuple[Subject, bool]: ...
    async def oidc(self, token: OIDCToken) -> tuple[Subject, bool]: ...
    async def persist(self, subject: Subject) -> None: ...
    async def sync(self, issuer: str, principal: PrincipalType) -> tuple[Subject, bool]: ...