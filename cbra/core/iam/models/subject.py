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
from typing import Literal

import pydantic

from cbra.types import ISessionManager
from cbra.types import PersistedModel
from ..types import PrincipalType
from .principal import Principal


class Subject(PersistedModel):
    kind: Literal['User']
    uid: int | None = pydantic.Field(
        default=None,
        auto_assign=True
    )

    created: datetime
    seen: datetime
    active: bool = True

    principals: set[Principal] = set()

    #: TODO: The PeristedModel must be refactored to register attribute mutations
    #: so that the storage backend can detect if it needs to delete something.
    _removed_principals: list[Principal] = pydantic.PrivateAttr([])

    def add_principal(
        self,
        issuer: str,
        value: PrincipalType,
        asserted: datetime,
        trust: bool = False
    ) -> None:
        assert self.uid is not None
        new = Principal.new(self.uid, issuer, value, asserted=asserted, trust=trust)
        old = None
        if new in self.principals:
            # TODO: ugly
            principals = list(self.principals)
            old = principals[principals.index(new)]
        must_add = any([
            old is None,
            old is not None and not old.trust
        ])
        if must_add:
            if old is not None:
                self._removed_principals.append(old)
                self.principals.remove(old)
            self.principals.add(new)

    def add_to_session(self, session: ISessionManager[Any]) -> None:
        raise NotImplementedError
    
    def has_principal(self, principal: PrincipalType) -> bool:
        p = Principal.new(
            0,
            '',
            principal,
            asserted=datetime.now(),
            trust=False
        )
        return p in self.principals