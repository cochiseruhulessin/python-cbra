# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
.. _ref-guides-persistence

=====================================
Storing and retrieving data with CBRA
=====================================
"""
from typing import Any
from typing import Protocol
from typing import TypeVar


I = TypeVar('I')
M = TypeVar('M')


class IModelRepository(Protocol[M]):
    model: type[M]

    async def allocate(self, model: type[Any], n: int = 1) -> int | list[int]:
        raise NotImplementedError

    def construct_key(self, model: Any) -> Any:
        raise NotImplementedError

    def restore(self, model: type[Any], entity: Any) -> Any:
        raise NotImplementedError

    async def get(self, identity: Any) -> M | None:
        raise NotImplementedError

    async def persist(self, instance: M) -> M:
        """Persist the model. When invoking this method, it is assumed that
        all necessary checks have been performed, so no validation is
        performed here.
        """
        raise NotImplementedError