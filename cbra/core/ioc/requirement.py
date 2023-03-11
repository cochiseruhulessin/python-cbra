# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable

from .container import Container
from .dependency import Dependency
from .dependencynotsatisfied import DependencyNotSatisfied


class Requirement:
    __module__: str = 'cbra.core.ioc'
    ref: Dependency | None = None
    missing: Any
    name: str

    @property
    def factory(self) -> Callable[..., Any]:
        dep = self.ref or self.missing
        assert dep is not None, self.name
        return dep.symbol

    def __init__(self, name: str, missing: Any = NotImplemented) -> None:
        self.missing = missing
        self.name = name

    def callable(self) -> bool:
        return False

    def add_to_container(self, container: Container) -> None:
        if self.ref is not None:
            return
        try:
            self.ref = container.require(self.name)
        except DependencyNotSatisfied:
            if self.missing in {NotImplemented, None}:
                raise
            self.ref = Dependency(
                name=self.name,
                qualname='NotImplemented',
                symbol=self.missing
            )

    def __repr__(self) -> str:
        return f'Requirement({self.name})'