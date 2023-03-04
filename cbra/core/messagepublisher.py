# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any

import aorta
import fastapi

from cbra.types import IDependant
from .ioc import instance
from .messagerunner import MessageRunner


class MessagePublisher(aorta.MessagePublisher, IDependant):
    __module__: str = 'cbra.core'
    logger: logging.Logger = logging.getLogger('aorta')
    request: fastapi.Request
    runner: MessageRunner

    def __init__(
        self,
        request: fastapi.Request,
        transport: aorta.types.ITransport = instance('MessageTransport')
    ):
        super().__init__(transport=transport)
        self.request = request

    async def send(
        self,
        messages: list[aorta.types.Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        for message in messages:
            self.logger.debug(
                "Publishing message %s/%s (id: %s)",
                message.api_version, message.kind, message.metadata.uid
            )
        return await super().send(messages, is_retry)