# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import inspect
import itertools
import types
from typing import Any

from cbra.types import IDependant
from cbra.types import IEndpoint
from cbra.types import IRequestPrincipal
from cbra.types import RequestPrincipal
from .requesthandler import RequestHandler
from .optionsrequesthandler import OptionsRequestHandler


class EndpointType(type):
    http_methods: list[str] = [
        'options',
        'head',
        'get',
        'post',
        'patch',
        'put',
        'delete',
        'trace'
    ]

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ) -> type[IEndpoint]:
        annotations = namespace.get('__annotations__') or {}
        is_abstract = namespace.pop('__abstract__', False)
        handlers: dict[str, RequestHandler[Any]] = collections.OrderedDict()

        # Inspect annotations for injectables.
        for attname, hint in annotations.items():
            if not inspect.isclass(hint)\
            or not issubclass(hint, IDependant)\
            or attname in namespace:
                continue
            namespace[attname] = hint.depends()

        if not is_abstract:
            for h in itertools.chain(*[getattr(x, 'handlers', {}) for x in bases]):
                handlers[h.attname] = h.clone() # type: ignore

            for attname, func in list(namespace.items()):
                if attname not in cls.http_methods:
                    continue
                if not callable(func):
                    raise TypeError("A request handler must be callable.")
                handlers[attname] = RequestHandler(
                    name=name,
                    method=attname,
                    func=func
                )

            namespace.update({
                'allowed_http_methods': [x.method for x in handlers.values()],
                'handlers': handlers.values()
            })

        # Create a concrete Principal subclass. This is to allow
        # thing like principal: RFC9068RequestPrincipal | OIDCRequestPrincipal.
        if annotations.get('principal') and not namespace.get('principal'):
            EndpointPrincipal: type[RequestPrincipal]
            principal: types.UnionType | IRequestPrincipal = annotations['principal']
            if isinstance(principal, types.UnionType):
                EndpointPrincipal = annotations['principal'] = type(
                    f'{name}Principal',
                    (RequestPrincipal,),
                    {'__annotations__': {'__root__': principal}}
                )
                namespace['principal'] = EndpointPrincipal.depends()


        Endpoint = super().__new__(cls, name, bases, namespace, **params)
        if not is_abstract:
            if 'OPTIONS' not in namespace['allowed_http_methods']\
            and getattr(Endpoint, 'with_options', True):
                # Create an options handler using the default CORS
                # policy.
                handlers['options'] = OptionsRequestHandler(name)
                namespace['allowed_http_methods'].append('OPTIONS')
        for handler in handlers.values():
            handler.add_to_class(Endpoint) # type: ignore
        return Endpoint # type: ignore