# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable
from typing import Callable
from typing import Iterable
from typing import TypeAlias
from typing import Union


__all__: list[str] = [
    'PolymorphicIterable'
]


PolymorphicIterable: TypeAlias = Union[
    Callable[..., Awaitable[Iterable[str]] | Iterable[str]],
    Iterable[str],
     None
]