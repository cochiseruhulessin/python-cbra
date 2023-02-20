# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
from typing import Any
from typing import Generic
from typing import TypeVar

from .icredential import ICredential


P = TypeVar('P')


class ICredentialVerifier(Generic[P]):
    """Knows how to verify a credential attached to a principal."""
    __module__: str = 'cbra.types'

    async def verify(
        self,
        principal: P,
        credential: ICredential | None,
        providers: set[str] | None = None
    ) -> bool:
        raise NotImplementedError