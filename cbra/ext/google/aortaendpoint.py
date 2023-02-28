# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any

import aorta

from .eventarcendpoint import EventarcEndpoint
from .messagediscarded import MessageDiscarded
from .messagerunner import MessageRunner
from .pubsubmessage import PubsubMessage


class AortaEndpoint(EventarcEndpoint):
    __module__: str = 'cbra.ext.google'
    runner: MessageRunner = MessageRunner.depends()

    async def on_message(self, message: PubsubMessage) -> None:
        try:
            data = message.get_data()
        except ValueError:
            self.logger.critical("Data could not be interpreted as JSON.")
            raise MessageDiscarded
        if data is None:
            raise MessageDiscarded
        envelope = aorta.parse(data)
        if envelope is None:
            self.logger.critical("Message is not an Aorta message type.")
            raise MessageDiscarded
        if not envelope.is_known():
            self.logger.critical(
                "Received an Aorta message of unknown type "
                "(kind: %s, version: %s, id: %s)",
                envelope.kind, envelope.api_version, envelope.metadata.uid
            )
            raise MessageDiscarded
        assert isinstance(envelope, aorta.types.Envelope)
        await self.runner.run(cast(aorta.types.Envelope[Any], envelope))