# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.ext.webhooks import BaseWebhookEndpoint
from cbra.ext.webhooks import WebhookResponse

from .shopifywebhookmessage import ShopifyWebhookMessage


class ShopifyWebhookEndpoint(BaseWebhookEndpoint):
    __module__: str = 'cbra.ext.shopify'
    domain: str = "shopify.com"
    summary: str = "Shopify"
    tags: list[str] = ["Webhooks (Incoming)"]

    async def post(
        self,
        message: ShopifyWebhookMessage = ShopifyWebhookMessage.depends()
    ) -> WebhookResponse:
        print(
            message.api_version,
            message.domain,
            message.hmac_sha256,
            message.topic,
            message.webhook_id
        )
        return self.on_success()