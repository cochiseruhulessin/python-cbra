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

import fastapi
import pydantic
from headless.ext.shopify import v2023_1

from cbra.types import IVerifier
from cbra.types import Request
from cbra.ext.webhooks import WebhookEnvelope


DEFAULT_API_VERSION: str = '2023-01'
MODELS: dict[tuple[str, str], type[pydantic.BaseModel]] = {
    ('2023-01', 'orders'): v2023_1.Order
}


class ShopifyWebhookEnvelope(WebhookEnvelope):
    __module__: str = 'cbra.ext.shopify'
    api_version: str
    content: dict[str, Any]
    domain: str
    hmac: bytes | None = None
    event_name: str
    webhook_id: str | None = None

    def __init__(
        self,
        api_version: str | None = fastapi.Header(
            default=None,
            alias='X-Shopify-API-Version',
        ),
        domain: str = fastapi.Header(
            default=None,
            alias='X-Shopify-Shop-Domain',
        ),
        signature: str = fastapi.Header(
            default=None,
            alias='X-Shopify-Hmac-Sha256',
        ),
        topic: str = fastapi.Header(
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
        self.hmac = signature.encode('utf-8')
        self.event_name = topic
        self.resource, self.event = str.split(topic, '/')
        self.webhook_id = webhook_id

    def get_message(self) -> pydantic.BaseModel:
        return MODELS[(self.api_version, self.resource)].parse_obj(self.content)

    async def verify(self, request: Request, verifier: IVerifier) -> bool:
        if self.hmac is None:
            return False
        return await verifier.verify(
            signature=self.hmac,
            message=await request.body(),
            encoder=base64.b64encode
        )