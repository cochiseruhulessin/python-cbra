# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.core import Endpoint

from .debugcommand import DebugCommand
from .debugevent import DebugEvent


class AortaDebugEndpoint(Endpoint):
    __module__: str = 'cbra.ext.google'
    include_in_schema: bool = False

    async def post(self) -> None:
        self.transaction.publish(DebugCommand())
        self.transaction.publish(DebugCommand(), audience={'self'})
        self.transaction.publish(DebugEvent())