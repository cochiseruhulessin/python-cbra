# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import re
from typing import Any
from typing import Callable

import fastapi

import cbra.core as cbra
from cbra.types import IVerifier
from .types import IWebhookEnvelope
from .webhookendpointtype import WebhookEndpointType
from .webhookresponse import WebhookResponse


class BaseWebhookEndpoint(cbra.Endpoint, metaclass=WebhookEndpointType):
    __module__: str = 'cbra.ext.shopify'
    domain: str
    envelope: Any
    with_options: bool = False
    function_reducers: list[Callable[[str], str]] = [
        lambda x: str.replace(x, '/', '_'),
        lambda x: str.replace(x, '-', '_'),
        lambda x: str.replace(x, '.', '_'),
        lambda x: re.sub('_+', '_', x),
        lambda x: str.lstrip(x, '_'),
        lambda x: str.rstrip(x, '_'),
    ]

    @classmethod
    def add_to_router(cls, router: fastapi.FastAPI, **kwargs: Any) -> None:
        kwargs.setdefault('path', f'/ext/{cls.domain}')
        return super().add_to_router(router, **kwargs)

    def get_handler_name(self, envelope: IWebhookEnvelope) -> str:
        return functools.reduce(
            lambda v, f: f(v),
            self.function_reducers,
            envelope.event_name
        )

    def reject(self, reason: str) -> WebhookResponse:
        return WebhookResponse(
            accepted=False,
            success=False,
            reason=reason
        )

    def _on_success(self) -> WebhookResponse:
        return WebhookResponse(
            accepted=True,
            success=True
        )

    async def get_message(self, envelope: IWebhookEnvelope) -> Any:
        """Return the message enclosed in the envelope. The default
        implementation simply returns the envelope.
        """
        return envelope

    async def get_verifier(self) -> IVerifier:
        raise NotImplementedError

    async def handle(self, envelope: IWebhookEnvelope) -> fastapi.Response | WebhookResponse:
        fn = getattr(self, f'on_{self.get_handler_name(envelope)}', None)
        if fn is None:
            return await self.sink(envelope)
        response = await fn(await self.get_message(envelope))
        if response and not isinstance(response, (fastapi.Response, WebhookResponse)):
            raise TypeError(
                f"The return value of {type(self).__name__}{fn.__name__} "
                "must be fastapi.Response or cbra.ext.webhooks.WebhookResponse."
            )
        return response or self._on_success()

    async def post(self) -> fastapi.Response | WebhookResponse:
        try:
            if not await self.verify(self.envelope):
                return self.reject("Signature validation failed.")
            return await self.handle(self.envelope)
        except Exception as exc:
            self.logger.exception("Caught fatal %s", type(exc).__name__)
            return self.reject("Caught fatal exception during message handling.")

    async def sink(self, envelope: IWebhookEnvelope) -> WebhookResponse:
        msg = f"No handler for event {envelope.event_name}"
        self.logger.critical(msg)
        return self.reject(msg)

    async def verify(self, envelope: IWebhookEnvelope) -> bool:
        return not self.require_authentication or await envelope.verify(
            request=self.request,
            verifier=await self.get_verifier()
        )