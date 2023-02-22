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
from .inheriteddependencydecorator import InheritDependenciesDecorator
from .injected import Injected
from .instance import Instance # type: ignore
from .requirement import Requirement
from .setting_ import Setting


__all__: list[str] = [
    'override',
    'inject',
    'instance',
    'setting',
    'Container',
    'Dependency',
    'Requirement',
]


def override(*args: Any, **kwargs: Any) -> Callable[..., Any]:
    """Injects the dependencies of the given callable."""
    return InheritDependenciesDecorator(*args, **kwargs)


def inject(name: str) -> Any:
    return Injected(name)


def instance(name: str, missing: Any = None) -> Any:
    return Instance(name, missing=missing)


def setting(name: str, default: Any = NotImplemented) -> Any:
    return Setting(name, missing=default)