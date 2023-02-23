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
from canonical import EmailAddress

from .principalmodel import PrincipalModel


class EmailPrincipal(PrincipalModel):
    kind: Literal['EmailAddress'] 
    email: EmailAddress = pydantic.Field(..., primary_key=True)

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        value: EmailAddress | None = values.pop('principal', None)
        if isinstance(value, EmailAddress):
            values['email'] = value
        return values
