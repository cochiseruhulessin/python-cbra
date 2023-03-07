# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import IDependant


DEFAULT_API_VERSION: str = '2023-01'


class ShopifyWebhookMessage(IDependant):
    __module__: str = 'cbra.ext.shopify'
    api_version: str
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
        )
    ):
        self.api_version = api_version or DEFAULT_API_VERSION
        self.domain = domain
        self.topic = topic
        self.webhook_id = webhook_id
        if signature is not None:
            self.hmac_sha256 = str.encode(signature, 'utf-8')