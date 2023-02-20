# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from collections import OrderedDict
from typing import Any
from typing import Callable
from typing import TypeVar


F = TypeVar('F', bound=Callable[..., Any])


class InheritDependenciesDecorator:
    parent: type[Any]
    signature: inspect.Signature

    def __init__(
        self,
        parent: type[Any]
    ):
        self.parent = parent
        self.signature = inspect.signature(parent)

    def __call__(
        self,
        func: F
    ) -> F:
        sig = inspect.signature(func)
        params: OrderedDict[str, inspect.Parameter] = OrderedDict([
            (name, param)
            for name, param in sig.parameters.items()
            if name not in ('args', 'kwargs')
        ])

        # Add the parameters of the parent, if it is not overriden
        # in the signature of func.
        for name, param in self.signature.parameters.items():
            if name in params or name in {'args', 'kwargs'}:
                continue
            params[name] = param
        func.__signature__ = sig.replace( # type: ignore
            parameters=list(params.values())
        )
        return func