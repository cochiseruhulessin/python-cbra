# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import runtime_checkable
from typing import Any
from typing import AsyncGenerator
from typing import Protocol

from .principal import Principal
from .principaltype import PrincipalType
from .subject import Subject


@runtime_checkable
class ISubjectRepository(Protocol):
    __module__: str = 'cbra.core.iam'

    async def find_by_principals(self, principals: list[Any]) -> set[int]: ...
    async def get(self, principal: int | PrincipalType) -> Subject: ...
    async def persist(self, subject: Subject) -> Subject: ...
    def get_principals(self, subject_id: int) -> AsyncGenerator[Principal, None]: ...