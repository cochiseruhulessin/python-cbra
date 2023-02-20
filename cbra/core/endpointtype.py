# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.types import IEndpoint
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
        is_abstract = namespace.pop('__abstract__', False)
        handlers: list[RequestHandler[Any]] = []
        if not is_abstract:
            for attname, func in list(namespace.items()):
                if attname not in cls.http_methods:
                    continue
                if not callable(func):
                    raise TypeError("A request handler must be callable.")
                handlers.append(
                    RequestHandler(
                        name=name,
                        method=attname,
                        func=func
                    )
                )

            namespace.update({
                'allowed_http_methods': [x.method for x in handlers],
                'handlers': handlers
            })
            if 'OPTIONS' not in namespace['allowed_http_methods']:
                # Create an options handler using the default CORS
                # policy.
                handlers.append(OptionsRequestHandler(name))
                namespace['allowed_http_methods'].append('OPTIONS')

        Endpoint = super().__new__(cls, name, bases, namespace, **params)
        for handler in handlers:
            handler.add_to_class(Endpoint) # type: ignore
        return Endpoint # type: ignore