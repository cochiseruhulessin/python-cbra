# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
from typing import Any
from typing import Awaitable

import fastapi

from cbra.types import IDependant
from cbra.types import IVerifier
from cbra.types import Request


DEFAULT_API_VERSION: str = '2023-01'


class ShopifyWebhookMessage(IDependant):
    __module__: str = 'cbra.ext.shopify'
    api_version: str
    content: dict[str, Any]
    domain: str | None
    hmac_sha256: bytes | None = None
    topic: str | None = None
    webhook_id: str | None = None

    def __init__(
        self,
        api_version: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-API-Version',
        ),
        domain: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-Shop-Domain',
        ),
        signature: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-Hmac-Sha256',
        ),
        topic: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-Topic'
        ),
        webhook_id: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-Webhook-Id'
        ),
        content: dict[str, Any] = fastapi.Body()
    ):
        self.api_version = api_version or DEFAULT_API_VERSION
        self.content = content
        self.domain = domain
        self.topic = topic
        self.webhook_id = webhook_id
        if signature is not None:
            self.hmac = base64.b64decode(str.encode(signature, 'utf-8'))

    def verify(self, request: Request, verifier: IVerifier) -> bool | Awaitable[bool]:
        return verifier.verify(self.hmac, request.sha256)