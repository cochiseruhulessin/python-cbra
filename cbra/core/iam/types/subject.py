# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from typing import Any
from typing import Protocol
from typing import TypeVar

from canonical import DomainName

from cbra.types import ISessionManager
from .principaltype import PrincipalType


T = TypeVar('T', bound='Subject')


class Subject(Protocol):
    uid: int | None
    seen: datetime

    def activate(self) -> None: ...
    def add_principal(self, issuer: str, value: PrincipalType, asserted: datetime, trust: bool = False) -> None: ...
    def add_to_session(self, session: ISessionManager[Any]) -> None: ...
    def can_destroy(self) -> bool: ...
    def has_principal(self, principal: PrincipalType) -> bool: ...
    def is_active(self) -> bool: ...
    def merge(self: T, other: T) -> None: ...
    def needs_fallback_email(self, allow: set[DomainName]) -> bool: ...