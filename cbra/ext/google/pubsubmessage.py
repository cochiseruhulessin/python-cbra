# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`PubsubMessage`."""
import datetime
import binascii
import base64
import json
from typing import Any

import pydantic


class PubsubMessage(pydantic.BaseModel):
    """A message that is published by publishers and consumed by subscribers.
    The message must contain either a non-empty `data` field or at least one
    attribute (in the `attributes` object). Note that client libraries represent
    this object differently depending on the language.
    """
    message_id: str = pydantic.Field(
        default=...,
        alias='messageId',
        title="Message ID",
        description=(
            "ID of this message, assigned by the server when the message is "
            "published. Guaranteed to be unique within the topic. This value "
            "may be read by a subscriber that receives a `PubsubMessage` via "
            "a `subscriptions.pull` call or a push delivery. It must not be "
            "populated by the publisher in a `topics.publish` call."
        )
    )

    publish_time: datetime.datetime = pydantic.Field(
        default=...,
        alias='publishTime',
        title="Published",
        description=(
            "The time at which the message was published, populated by Google "
            "Pub/Sub when it receives the `topics.publish` call. It must not "
            "be populated by the publisher in a `topics.publish` call.\n\nA "
            "timestamp in RFC3339 UTC \"Zulu\" format, with nanosecond "
            "resolution and up to nine fractional digits. Examples: `2014-10-"
            "02T15:01:23Z` and `2014-10-02T15:01:23.045123456Z`."
        )
    )
    attributes: dict[str, Any] | None = pydantic.Field(
        default=None,
        title="Attributes",
        description=(
            "Attributes for this message. If this field is empty, the "
            "message contains non-empty data. This can be used to filter "
            "messages on the subscription.\n\n"
            "An object containing a list of `key`: `value` pairs. Example: "
            "`{ \"name\": \"wrench\", \"mass\": \"1.3kg\", \"count\": \"3\" }`."
        )
    )

    data: str | None = pydantic.Field(
        default=None,
        title="Data",
        description=(
            "The message data field. If this field is empty, the message "
            "contains at least one attribute.\n\nA base64-encoded string."
        )
    )

    def get_data(self) -> Any:
        """Return a dictionary or a list containing the message
        data as specified by the ``.data`` attribute. The encoding
        is assumed JSON/UTF-8.
        """
        if self.data is None: # pragma: no cover
            return None
        try:
            return json.loads(base64.b64decode(self.data))
        except (binascii.Error, json.decoder.JSONDecodeError, TypeError):
            raise ValueError
