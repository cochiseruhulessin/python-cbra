# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from types import NotImplementedType
from typing import Any

import pydantic
from ckms.jose import Decoder
from ckms.types import Malformed


class JSONWebTokenPrincipal(pydantic.BaseModel):
    token: str

    @classmethod
    def parse_jwt(
        cls,
        token: str,
        accept: set[str] | NotImplementedType = NotImplemented
    ) -> dict[str, Any]:
        typ = None
        try:
            jose, jwt = Decoder.introspect(token)
        except Malformed:
            raise ValueError('malformed JSON Web Token')
        for header in jose.headers:
            if header.typ is None:
                continue
            typ = str.lower(header.typ)
            break
        else:
            typ = None
        if jwt is None:
            raise ValueError('could not decode JSON Web Token.')
        if typ is None:
            raise ValueError('untyped JWT can not be used as an access token.')
        if accept != NotImplemented and typ not in accept:
            raise TypeError(f'Invalid JWT type: {typ[:16]}')
        return {**jwt.dict(), 'token': token}