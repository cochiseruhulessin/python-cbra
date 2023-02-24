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
        if old is None or not old.trust:
            self.principals.add(new)

    def add_to_session(self, session: ISessionManager[Any]) -> None:
        raise NotImplementedError