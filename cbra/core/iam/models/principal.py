# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from typing import TypeAlias
from typing import Union

import pydantic

from cbra.types import PersistedModel
from ..types import PrincipalType

from .emailprincipal import EmailPrincipal
from .externalprincipal import ExternalPrincipal
from .publicidentifierprincipal import PublicIdentifierPrincipal


PrincipalSpecType: TypeAlias = Union[
    EmailPrincipal,
    ExternalPrincipal,
    PublicIdentifierPrincipal
]


class Principal(PersistedModel):
    id: int | None = pydantic.Field(
        default=None,
        auto_assign=True
    )
    spec: PrincipalSpecType = pydantic.Field(..., primary_key=True)
    subject: int
    asserted: datetime
    suspended: bool = False

    @classmethod
    def new(
        cls,
        subject: int,
        issuer: str,
        principal: PrincipalType,
        asserted: datetime
    ):
        return cls.parse_obj({
            'asserted': asserted,
            'subject': subject,
            'spec': {
                'iss': issuer,
                'kind': type(principal).__name__,
                'principal': principal,
            }
        })