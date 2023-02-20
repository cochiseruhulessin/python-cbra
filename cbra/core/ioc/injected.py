# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import inspect
from typing import Any

import fastapi.params

from .requirement import Requirement


class Injected(Requirement, fastapi.params.Depends):
    _is_coroutine = asyncio.coroutines._is_coroutine # type: ignore

    @property
    def __signature__(self) -> inspect.Signature:
        return inspect.Signature()

    def __init__(self, name: str, missing: Any | None = NotImplemented):
        Requirement.__init__(self, name=name, missing=missing)
        fastapi.params.Depends.__init__(
            self,
            dependency=self,
            use_cache=False
        )

    async def resolve(self, *args: Any, **kwargs: Any) -> Any:
        assert self.ref is not None
        return self.ref.symbol

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return await self.resolve(*args, **kwargs)