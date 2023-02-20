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

from .injected import Injected


class Instance(Injected):

    @property
    def __signature__(self) -> inspect.Signature:
        assert self.ref is not None
        return inspect.signature(self.factory)

    def callable(self) -> bool:
        return True

    async def resolve(self, *args: Any, **kwargs: Any) -> Any:
        assert self.ref is not None
        return self.ref.init(*args, **kwargs)