# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable
from typing import Callable
from typing import TypeVar

import fastapi


T = TypeVar('T', bound='IDependant')


class IDependant:
    __module__: str = 'cbra.types'

    @classmethod
    def depends(cls: type[T]) -> T:
        """Return a :class:`fastapi.params.Depends` object."""
        return fastapi.Depends(cls.__inject__())

    @classmethod
    def __inject__(cls: type[T]) -> Callable[..., Awaitable[T] | T]:
        """Return a callable that specifies the dependencies of this
        class in its signature.
        """
        return cls