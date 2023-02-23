# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from headless.ext.oauth2.models import OIDCToken

from .subject import Subject


class IUserOnboardingService(Protocol):
    def initialize(self) -> Subject: ...
    async def oidc(self, token: OIDCToken) -> tuple[Subject, bool]: ...
    async def update(self, subject: Subject) -> None: ...