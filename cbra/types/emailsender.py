# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol


class EmailSender(Protocol):
    __module__: str = 'cbra.types'

    async def send(
        self,
        sender: str,
        recipients: list[str],
        subject: str,
        content: list[str],
        headers: dict[str, Any] | None = None
    ) -> None:
        ...