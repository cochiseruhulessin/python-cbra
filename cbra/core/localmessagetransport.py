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
from aorta.types import Envelope

from .messagepublisher import MessagePublisher
from .messagerunner import MessageRunner


class LocalMessageTransport:
    __module__: str = 'aorta'
    runner: MessageRunner

    def __init__(
        self,
        request: fastapi.Request
    ):
        self.publisher = MessagePublisher(request=request, transport=self)
        self.runner = MessageRunner(request=request, publisher=self.publisher)

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        for message in messages:
            await self.runner.run(message)