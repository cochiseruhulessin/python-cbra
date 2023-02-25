# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hmac


class WebhookSecret:
    __module__: str = 'cbra.ext.picqer'

    def __init__(self, secret: bytes | str):
        if isinstance(secret, str):
            secret = str.encode(secret, 'ascii')
        assert isinstance(secret, bytes)
        self.__secret = secret

    async def verify(
        self,
        signature: bytes,
        message: bytes,
    ) -> bool:
        return hmac.compare_digest(
            hmac.digest(self.__secret, message, 'sha256'),
            signature
        )