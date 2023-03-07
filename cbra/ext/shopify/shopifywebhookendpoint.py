# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.webhooks import WebhookEndpoint

from .shopifywebhookmessage import ShopifyWebhookMessage


class ShopifyWebhookEndpoint(WebhookEndpoint):
    __module__: str = 'cbra.ext.shopify'
    domain: str = "shopify.com"
    envelope: ShopifyWebhookMessage
    require_authentication: bool = False
    summary: str = "Shopify"
    tags: list[str] = ["Webhooks (Incoming)"]

    async def on_order_created(
        self,
        envelope: ShopifyWebhookMessage
    ) -> None:
        print(self.request.sha256)
        print(
            envelope.api_version,
            envelope.domain,
            envelope.hmac_sha256,
            envelope.topic,
            envelope.webhook_id,
            envelope.content
        )