# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from .loader import import_symbol


class Dependency(pydantic.BaseModel):
    name: str
    qualname: str
    symbol: Any = None
    instance: Any = None
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    singleton: bool = False

    def init(self, *args: Any, **kwargs: Any) -> Any:
        assert self.symbol is not None
        return self.instance or self.symbol(*args, **kwargs)

    def resolve(self) -> None:
        try:
            self.symbol = import_symbol(self.qualname)
        except ImportError:
            raise
        if self.singleton:
            self.instance = self.symbol(*self.args, **self.kwargs)