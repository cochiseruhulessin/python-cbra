# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
import binascii

import fastapi

from cbra.types import IDependant
from cbra.types import Verifier


class WebhookSignature(IDependant):
    __module__: str = 'cbra.ext.picqer'
    request: fastapi.Request
    digest: bytes | None = None

    def __init__(
        self,
        request: fastapi.Request,
        digest: str | None = fastapi.Header(
            default=None,
            alias='X-Picqer-Signature',
            title='Signature',
            description=(
                'A Base64-encoded SHA256 hash of the request body that was '
                'created using a shared secret.'
            )
        )
    ) -> None:
        self.request = request
        self.signature = None
        if digest:
            try:
                self.signature = base64.urlsafe_b64decode(str.encode(digest))
            except (binascii.Error, TypeError, ValueError):
                pass

    async def verify(
        self,
        verifier: Verifier
    ) -> bool:
        body = await self.request.body()
        if self.signature is None or not body:
            return False
        return await verifier.verify(self.signature, body)

    def __bool__(self) -> bool:
        return bool(self.signature)