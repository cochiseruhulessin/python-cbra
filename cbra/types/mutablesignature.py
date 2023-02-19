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
from typing import TypeVar
from inspect import Signature


T = TypeVar('T', bound='MutableSignature')


class MutableSignature:
    """Exposes an interface to mutate signatures."""
    __module__: str = 'cbra.types'

    @classmethod
    def fromfunction(cls: type[T], func: Any) -> T:
        return cls(func, inspect.signature(func))

    @property
    def named(self) -> list[inspect.Parameter]:
        """The list of named arguments that are not ``self``
        or variable.
        """
        params = list(self.sig.parameters.values())
        return [x for x in params if x.name not in {'args', 'kwargs', 'self'}]

    @property
    def return_annotation(self) -> Any:
        return self.sig.return_annotation

    def __init__(self, obj: Any, signature: Signature):
        self.obj = obj
        self.sig = signature

    def clear(self) -> None:
        """Remote the positional and keyword arguments from the
        signature.
        """
        pass

    def has_param(self, name: str) -> bool:
        """Return a boolean indicating if the signature has the given
        named parameter.
        """
        return name in self.sig.parameters