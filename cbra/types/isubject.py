# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from canonical import EmailAddress

from .icredentialverifier import ICredentialVerifier


class ISubject:
    """Represents an identfied subject, its principal and its
    credential.
    """
    __module__: str = 'cbra.types'
    email: EmailAddress | None
    sub: Any

    def is_authenticated(self) -> bool:
        raise NotImplementedError

    async def authenticate(
        self,
        verifier: ICredentialVerifier[Any],
        providers: set[str] | None = None
    ) -> None:
        """Authenticate the subject."""
        raise NotImplementedError

    def has_claim(self, name: str, value: Any) -> bool:
        raise NotImplementedError