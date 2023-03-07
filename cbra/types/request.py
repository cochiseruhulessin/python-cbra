# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
import hmac

import fastapi


class Request(fastapi.Request):
    __module__: str = 'cbra.core'

    @property
    def sha256(self) -> bytes:
        if not hasattr(self, "_body"):
            raise ValueError("Body not available")
        return hashlib.sha256(self._body).digest()
    
    def hmac(self, secret: bytes, algorithm: str = 'sha256') -> bytes:
        assert self._body is not None
        return hmac.digest(secret, self._body, algorithm)