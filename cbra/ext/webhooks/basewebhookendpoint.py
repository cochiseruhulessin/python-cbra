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
import pydantic

import cbra.core as cbra
from cbra.types import IVerifier
from .notimplementedenvelope import NotImplementedEnvelope
from .types import IWebhookEnvelope
from .types import WebhookException
from .types import WebhookResponse
from .webhookendpointtype import WebhookEndpointType


class BaseWebhookEndpoint(cbra.Endpoint, metaclass=WebhookEndpointType):
    __module__: str = 'cbra.ext.shopify'
    domain: str
    envelope: IWebhookEnvelope = NotImplementedEnvelope.depends()
    require_authentication: bool = False
    signed: bool = False
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
        if envelope.event_name == NotImplemented:
            raise NotImplementedError
        return functools.reduce(
            lambda v, f: f(v),
            self.function_reducers,
            envelope.event_name
        )

    def reject(self, reason: str, code: str | None = None) -> WebhookResponse:
        return WebhookResponse(
            accepted=False,
            success=False,
            reason=reason,
            code=code
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
        return envelope.get_message()

    async def get_verifier(self) -> IVerifier:
        raise NotImplementedError

    async def handle(self, envelope: IWebhookEnvelope) -> WebhookResponse:
        fn = getattr(self, f'on_{self.get_handler_name(envelope)}', None)
        if fn is None:
            return await self.sink(envelope)
        try:
            message = await self.get_message(envelope)
        except pydantic.ValidationError:
            self.logger.critical("Unable to parse webhook message.")
            return self.reject("Unknown message format.", "UNKNOWN_MESSAGE_FORMAT")
        response = await fn(message)
        if response and not isinstance(response, WebhookResponse):
            raise TypeError(
                f"The return value of {type(self).__name__}{fn.__name__} "
                "must be cbra.ext.webhooks.WebhookResponse."
            )
        return response or self._on_success()

    async def post(self) -> WebhookResponse:
        try:
            if not await self.verify(self.envelope):
                self.logger.critical(
                    "Signature validation failed for message received by %s",
                    type(self).__name__
                )
                return self.reject("Signature validation failed.", "INVALID_SIGNATURE")
            return await self.handle(self.envelope)
        except WebhookException:
            self.logger.critical("Caught WebhookException")
            raise
        except Exception as exc:
            self.logger.exception("Caught fatal %s", type(exc).__name__)
            return self.reject(
                "Caught fatal exception during message handling.",
                'FATAL_EXCEPTION'
            )

    async def sink(self, envelope: IWebhookEnvelope) -> WebhookResponse:
        msg = f"No handler for event {envelope.event_name}"
        self.logger.critical(msg)
        return self.reject(msg)

    async def verify(self, envelope: IWebhookEnvelope) -> bool:
        return not self.signed or await envelope.verify(
            request=self.request,
            verifier=await self.get_verifier()
        )