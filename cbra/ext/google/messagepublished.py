# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`MessagePublished`."""
import pydantic

from .pubsubmessage import PubsubMessage

SUBSCRIPTION_NAME_REGEX = r'^projects/[\-a-z0-9]{6,30}/subscriptions/.*$'


class MessagePublished(pydantic.BaseModel):
    """A datastructure containing a message that was published to a Google Pub/Sub
    topic and received by the server through a subscription.
    """
    subscription: str = pydantic.Field(
        default=...,
        title="Subscription",
        description=(
            "The subscription through which the message was delivered to the "
            "endpoint."
        ),
        regex=SUBSCRIPTION_NAME_REGEX,
        example="projects/myproject/subscriptions/mysub"
    )

    message: PubsubMessage
