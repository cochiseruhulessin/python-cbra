# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Literal

import pydantic

from ..types import PublicIdentifier
from .principalmodel import PrincipalModel


class PublicIdentifierPrincipal(PrincipalModel):
    kind: Literal['PublicIdentifier']
    iss: str = pydantic.Field(..., primary_key=True)
    sub: str = pydantic.Field(..., primary_key=True)

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        value: PublicIdentifier | None = values.pop('principal', None)
        if isinstance(value, PublicIdentifier):
            values.update({
                'iss': value.iss,
                'sub': value.sub
            })
        return values