# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .icredential import ICredential
from .verifier import Verifier


class HMACSignature(ICredential):
    __module__: str = 'cbra.types'

    def __init__(self, signature: bytes, message: bytes):
        self.message = message
        self.signature = signature

    async def verify(self, verifier: Verifier) -> bool:
        return await verifier.verify(self.signature, self.message)