# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import get_args
from typing import Callable

import fastapi
from headless.ext.picqer import Client
from headless.ext.picqer import DefaultClient
from headless.ext.picqer.v1 import Webhook

import cbra.core
from cbra import types
from cbra.core.conf import settings

from .webhooksignature import WebhookSignature
from .webhookresponse import WebhookResponse
from .webhooksecret import WebhookSecret
from .v1 import PicqerWebhookMessage


class PicqerWebhookEndpoint(cbra.core.Endpoint):
    __module__: str = 'cbra.ext.picqer'
    client: Client = fastapi.Depends(DefaultClient)
    tags: list[str] = ['Integrations']
    name: str = 'picqer.webhooks'
    summary: str = 'Picqer Webhooks'
    with_options: bool = False
    signature: WebhookSignature = WebhookSignature.depends()

    @classmethod
    async def install(
        cls,
        client: Client,
        callback_url: str,
        generate_name: Callable[[str], str],
        secret: str | None = None,
        skip_missing: bool = True
    ):
        """Install webhooks created by this server."""
        # Inspect the types to get the supported Picqer event types.
        events: set[str] = set()
        for model in get_args(PicqerWebhookMessage):
            for event in get_args(model.__fields__['event'].type_):
                fn = f"on_{str.replace(event, '.', '_')}"
                if not hasattr(cls, fn) and skip_missing:
                    cls.logger.debug(
                        'Event %s is not implemented by %s',
                        event, cls.__name__
                    )
                    continue
                events.add(event)

        # Fetch all webhooks and determine determine which ones we
        # need to create.
        async for hook in client.listall(Webhook):
            if not hook.active:
                continue
            if hook.name != generate_name(hook.event):
                continue
            events.remove(hook.event)
        
        # The remaining hooks need to be created.
        for event in sorted(events):
            cls.logger.warning("Creating webhook for event %s", event)
            params: dict[str, str] = {
                'name': generate_name(event),
                'event': event,
                'address': callback_url
            }
            if secret:
                params['secret'] = secret
            await client.post(
                url=Webhook.get_create_url(),
                json=params
            )

    async def post(self, dto: PicqerWebhookMessage) -> WebhookResponse:
        if not await self.signature.verify(await self.get_webhook_secret()):
            raise types.Forbidden
        attname = f"on_{str.replace(dto.event, '.', '_')}"
        if not hasattr(self, attname):
            self.logger.critical(
                'Picqer event %s is not implemented by this endpoint.',
                dto.event
            )
            return self.reject(reason=f"This server does not implement {dto.event}")
        func = getattr(self, attname)
        try:
            return await func(dto) or WebhookResponse(
                accepted=True,
                success=True
            )
        except Exception:
            self.logger.exception("Caught fatal exception while handling webhook message")
            return WebhookResponse(
                accepted=True,
                success=False
            )

    async def get_webhook_secret(self) -> types.Verifier:
        return WebhookSecret(settings.PICQER_WEBHOOK_SECRET) # type: ignore

    def reject(self, reason: str) -> WebhookResponse:
        return WebhookResponse(accepted=False, success=False, reason=reason)