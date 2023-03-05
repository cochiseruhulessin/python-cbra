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

import aorta


class IOriginStorage(Protocol):
    __module__: str = 'cbra.ext.origin.types'

    async def latest(self) -> aorta.types.Envelope[Any]:
        ...

    async def persist(
        self,
        message: aorta.types.Envelope[Any]
    ) -> None:
        ...

    async def seen(
        self,
        message: aorta.types.Envelope[Any]
    ) -> bool:
        ...