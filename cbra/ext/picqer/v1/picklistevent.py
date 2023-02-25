# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

from headless.ext.picqer.v1 import Picklist

from .event import Event


class PicklistEvent(Event):
    event: Literal[
        "picklists.created",
        "picklists.closed",
        "picklists.cancelled",
        "picklists.snoozed",
        "picklists.unsnoozed",
    ]

    data: Picklist
