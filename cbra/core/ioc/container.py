# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
from typing import Any
from typing import TypeVar

from .dependency import Dependency
from .dependencynotsatisfied import DependencyNotSatisfied


T = TypeVar('T', bound='Container')


class Container:
    """Holds injected dependencies."""
    __module__: str = 'cbra.core.ioc'
    injected: dict[str, Any] = collections.OrderedDict()
    requirements: set[str]

    @classmethod
    def fromsettings(cls: type[T]) -> T:
        from cbra.core.conf import settings
        container = cls()
        for dependency in getattr(settings, 'DEPENDENCIES', []):
            container.add(Dependency.parse_obj(dependency))
        return container

    def __init__(self):
        self.injected = collections.OrderedDict()
        self.requirements = set()

    def add(self, dependency: Dependency):
        dependency.resolve()
        self.injected[dependency.name] = dependency

    def require(self, name: str) -> Dependency:
        if name not in self.injected:
            raise DependencyNotSatisfied
        return self.injected[name]