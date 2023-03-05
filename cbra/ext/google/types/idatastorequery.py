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


class IDatastoreQuery(Protocol):
    __module__: str = 'cbra.ext.google.types'
    def add_filter(self, attname: str, op: str, value: Any) -> None: ...
    def keys_only(self) -> bool: ...
    def fetch(self) -> None: ...