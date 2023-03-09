# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hmac
from typing import Callable

from cbra.types import IVerifier


class HMACWebhookVerifier(IVerifier):
    __module__: str = 'cbra.ext.webhooks'
    algorithm: str

    def __init__(self, secret: bytes, algorithm: str):
        self.algorithm = algorithm
        self.__secret = secret

    async def verify(
        self,
        signature: bytes,
        message: bytes,
        encoder: Callable[[bytes], bytes] = lambda x: x
    ) -> bool:
        return hmac.compare_digest(
            encoder(hmac.digest(self.__secret, message, self.algorithm)),
            signature
        )
    

class HMACSHA256WebhookVerifier(HMACWebhookVerifier):
    __module__: str = 'cbra.ext.webhooks'

    def __init__(self, secret: bytes):
        super().__init__(secret=secret, algorithm='sha256')