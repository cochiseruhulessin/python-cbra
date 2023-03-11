# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from ckms.core import Keychain
from ckms.jose import PayloadCodec

from cbra.types import IDependant
from ..const import DEFAULT_SIGNING_KEY
from .serverkeychain import ServerKeychain




class TokenSigner(IDependant):
    __module__: str = 'cbra.ext.oauth2.params'
    keychain: Keychain

    def __init__(self, keychain: Keychain = ServerKeychain):
        self.codec = PayloadCodec(
            signer=keychain,
            signing_keys=[DEFAULT_SIGNING_KEY]
        )
        self.keychain = keychain

    async def jwt(
        self,
        claims: dict[str, Any],
        typ: str = 'jwt'
    ) -> str:
        return await self.codec.encode(
            payload=claims,
            content_type=typ
        )