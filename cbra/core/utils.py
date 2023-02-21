# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar


_T = TypeVar('_T')


def parent_signature(f: _T) -> Callable[[Any], _T]:
    def decorator_factory(func: Callable[[Any], _T]) -> _T:
        sig = inspect.signature(f) # type: ignore
        func.__signature__ = sig # type: ignore
        return func # type: ignore
    return decorator_factory


async def ensure_awaited(obj: _T | Awaitable[_T], default: Any = NotImplemented) -> _T:
    if inspect.isawaitable(obj):
        value: _T = await obj
    else:
        value = obj # type: ignore
    if not value and (default != NotImplemented):
        value = default
    return value