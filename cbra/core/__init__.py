# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Callable
from typing import TypeVar

from pydantic import Field

from .application import Application
from .endpoint import Endpoint
from . import ioc
from .params import *
from .resource import Create
from .resource import Delete
from .resource import Mutable
from .resource import Replace
from .resource import Resource
from .resource import ResourceModel
from .resource import ResourceType
from .resource import Retrieve
from .resource import Update
from .secretkey import SecretKey


T = TypeVar('T')


__all__: list[str] = [
    'describe',
    'inject',
    'instance',
    'ioc',
    'permission',
    'Application',
    'ApplicationSecretKey',
    'Create',
    'Delete',
    'Endpoint',
    'Field',
    'Mutable',
    'Replace',
    'Resource',
    'ResourceModel',
    'ResourceType',
    'Retrieve',
    'SecretKey',
    'Update'
]

inject = ioc.inject
instance = ioc.instance
permission = Endpoint.require_permission


class describe:
    status_code: int = 200

    def __init__(
        self,
        status_code: int = 200
    ) -> None:
        self.status_code = status_code

    def __call__(
        self,
        func: Callable[..., T]
    ) -> Callable[..., T]:
        if not hasattr(func, 'params'):
            func.params = {} # type: ignore
        func.params.update(self.__dict__) # type: ignore
        return func