# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generator
from typing import TypeVar


T = TypeVar('T', bound='IDeferred')


class IDeferred:
    __module__: str = 'cbra.types'

    async def initialize(self) -> None:
        raise NotImplementedError

    async def _initialize(self: T) -> T:
        await self.initialize()
        return self

    def __await__(self: T) -> Generator[None, None, T]:
        return self._initialize().__await__()