# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .icredentialverifier import ICredentialVerifier
from .isubject import ISubject


class NullSubject(ISubject):
    """An :class:`ISubject` implementation that represents an non-authenticated
    and non-identified subject.
    """
    __module__: str = 'cbra.types'
    email: None = None
    sub: None = None

    def is_authenticated(self) -> bool:
        return False

    async def authenticate(
        self,
        verifier: ICredentialVerifier[Any],
        providers: set[str] | None = None
    ) -> None:
        return

    def has_claim(self, name: str, value: Any) -> bool:
        return False