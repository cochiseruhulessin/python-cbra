# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar

from .resourcemodel import ResourceModel

T = TypeVar('T', bound=ResourceModel)


class QueryResult(Generic[T]):
    __module__: str = 'cbra.core'
    token: str | None

    def __init__(self, token: str | None, items: list[T]):
        self.token = token or None
        self.items = items