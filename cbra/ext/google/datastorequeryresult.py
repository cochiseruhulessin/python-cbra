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


T = TypeVar('T')


class DatastoreQueryResult(Generic[T]):
    __module__: str = 'cbra.ext.google'
    token: str | None
    items: list[T]

    def __init__(self, token: str | None, entities: list[T]) -> None:
        self.token = token or None
        self.items = entities