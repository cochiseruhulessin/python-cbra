# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import hashlib
from typing import Any

from canonical import EmailAddress
from headless.ext.oauth2.models import SubjectIdentifier

from .types import PublicIdentifier
from .types import PrincipalType


class PrincipalHasher:
    """Known how to create a unique hash of a given principal."""
    __module__: str = 'cbra.core.iam'

    #: The algorithm that is used to hash principals.
    #:
    #: .. warning::
    #:
    #:   Changing this for an existing dataset will cause duplicate
    #:   principals.
    algorithm: str = 'sha1'

    def create_hasher(self) -> Any:
        # We use SHA-1 here because its unique enough, as it will
        # be applied on data that is already being constrained
        # such as email addresses or phone numbers. If there is
        # a collision then the user just has bad luck.
        return hashlib.new(self.algorithm)

    @functools.singledispatchmethod
    def hash(
        self,
        principal: PrincipalType,
    ) -> str:
        """Create a hash of the given principal."""
        raise NotImplementedError(type(principal).__name__)

    @hash.register # type: ignore
    def hash_email(
        self,
        principal: EmailAddress
    ) -> str:
        h = self.create_hasher()
        h.update(str.encode(type(principal).__name__, 'ascii'))
        h.update(str.encode(principal))
        return self._format(h.hexdigest())

    @hash.register # type: ignore
    def hash_subject_identifier(
        self,
        principal: SubjectIdentifier
    ) -> str:
        h = self.create_hasher()
        h.update(str.encode(type(principal).__name__, 'ascii'))
        h.update(str.encode(principal.iss))
        h.update(str.encode(principal.sub))
        return self._format(h.hexdigest())

    @hash.register # type: ignore
    def hash_public_identifier(
        self,
        principal: PublicIdentifier
    ) -> str:
        h = self.create_hasher()
        h.update(str.encode(type(principal).__name__, 'ascii'))
        h.update(str.encode(principal.iss))
        h.update(str.encode(principal.sub))
        return self._format(h.hexdigest())
    
    def _format(self, v: str) -> str:
        return f'{self.algorithm}:{v}'