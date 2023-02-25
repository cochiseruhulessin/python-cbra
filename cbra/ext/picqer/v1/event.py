# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pydantic


class Event(pydantic.BaseModel):
    idhook: int = pydantic.Field(
        default=...,
        title="Webhook ID",
        description=(
            'Identifies the webhook that produced the incoming '
            'message.'
        )
    )

    name: str = pydantic.Field(
        default=...,
        title='Name',
        description=(
            'The name of the webhook as created in the Picqer '
            'application.'
        )
    )

    event_triggered_at: datetime.datetime = pydantic.Field(
        default=...,
        title="Timestamp",
        description=(
            'The date and time at which the event was triggered.'
        )
    )

    event: str