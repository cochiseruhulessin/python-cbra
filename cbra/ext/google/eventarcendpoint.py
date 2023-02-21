# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`EventarcEndpoint`."""
from .googleendpoint import GoogleEndpoint
from .messagepublished import MessagePublished
from .pubsubmessage import PubsubMessage


class EventarcEndpoint(GoogleEndpoint):
    """Accepts a message from Google Eventarc from a HTTP POST request. The
    default implementation does nothing. Implementations must override
    the :meth:`on_message()` method to handle the incoming messages.
    """
    __module__: str = 'cbra.ext.google'
    include_in_schema: bool = False
    status_code: int = 201
    summary: str = 'Eventarc Message'
    tags: list[str] = ['Cloud Endpoints']

    async def post(self, dto: MessagePublished) -> None:
        """Receive a `google.cloud.pubsub.topic.v1.messagePublished` message
        and invoke the appropriate handler.
        """
        self.logger.debug(
            "Received message %s from Google Pub/Sub",
            dto.message.message_id
        )
        return await self.on_message(dto.message)

    async def on_message(self, message: PubsubMessage) -> None:
        """Handles the message received from Google Pub/Sub. The default
        implementation does nothing
        """
        return