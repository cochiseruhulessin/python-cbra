# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

import cbra.core as cbra
from .webhookresponse import WebhookResponse


class BaseWebhookEndpoint(cbra.Endpoint):
    __module__: str = 'cbra.ext.shopify'
    domain: str
    with_options: bool = False

    @classmethod
    def add_to_router(cls, router: fastapi.FastAPI, **kwargs: Any) -> None:
        kwargs.setdefault('path', f'/ext/{cls.domain}')
        return super().add_to_router(router, **kwargs)

    def on_success(self) -> WebhookResponse:
        return WebhookResponse(
            accepted=True,
            success=True
        )