# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import TypeAlias

from cbra.core import EndpointType
from cbra.types import IEndpoint


class WebhookEndpointType(EndpointType):
    __module__: str = 'cbra.ext.webhooks'

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> type[IEndpoint]:
        # Do not pop
        annotations: dict[str, type] = namespace.get('__annotations__') or {}
        is_abstract = namespace.get('__abstract__', False)
        if not is_abstract:
            envelope: Any = None
            for b in reversed(bases):
                if not isinstance(b, WebhookEndpointType):
                    continue
                if not b.__annotations__.get('envelope'): # pragma: no cover
                    continue
                envelope = b.__annotations__.get('envelope')
            envelope = cast(TypeAlias, annotations.setdefault('envelope', envelope))
            if envelope is None: # pragma: no cover
                raise TypeError("Define a message envelope")
        new_class = super().__new__(cls, name, bases, namespace, **params)
        #if not is_abstract:
        #    if not hasattr(new_class, 'domain'):
        #        raise TypeError(f'{name}.domain must be declared.')
        return new_class