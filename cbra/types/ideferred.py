# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Generator
from typing import TypeVar


T = TypeVar('T', bound='IDeferred')


class IDeferred:
    __module__: str = 'cbra.types'

    @classmethod
    def defer(cls: type[T], obj: T, name: str) -> Any:
        return cls.DeferredAttribute(obj, name)

    async def initialize(self) -> None:
        raise NotImplementedError

    async def _initialize(self: T) -> T:
        await self.initialize()
        return self

    def __await__(self: T) -> Generator[None, None, T]:
        return self._initialize().__await__()

    class DeferredAttribute:

        def __init__(self, obj: 'IDeferred', name: str):
            self.obj = obj
            self.name = name

        def __getattr__(self, __name: str) -> Any:
            raise RuntimeError(
                f'Await {type(self.obj).__name__} before accessing attribute '
                f'{type(self.obj).__name__}.{self.name}.{__name}.'
            )

        __repr__ = lambda self: self.__getattr__('__repr__') # type: ignore