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
from .messagepublisher import MessagePublisher
from .params import *
from .resource import Collection
from .resource import Create
from .resource import Delete
from .resource import Mutable
from .resource import QueryResult
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
    'Collection',
    'Create',
    'Delete',
    'Endpoint',
    'Field',
    'MessagePublisher',
    'Mutable',
    'QueryResult',
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
    summary: str | None = None

    def __init__(
        self,
        status_code: int = 200,
        summary: str | None = None
    ) -> None:
        self.status_code = status_code

    def __call__(
        self,
        func: Callable[..., T]
    ) -> Callable[..., T]:
        if not hasattr(func, 'params'):
            func.params = {} # type: ignore
        func.params.update({ # type: ignore
            k: v for k, v in self.__dict__.items()
            if v is not None
        })
        return func


class action:
    """Like :class:`describe`, but decorates the method to indicate that
    it exposes an action on a resource.
    """
    action: str
    method: str
    name: str
    status_code: int = 200
    summary: str | None = None

    def __init__(
        self,
        summary: str,
        *,
        method: str,
        status_code: int = 200,
    ) -> None:
        self.method = method
        self.status_code = status_code
        self.summary = summary

    def __call__(
        self,
        func: Callable[..., T]
    ) -> Callable[..., T]:
        self.action = func.__name__
        func.action = {} # type: ignore
        func.action.update({ # type: ignore
            k: v for k, v in self.__dict__.items()
            if v is not None
        })
        return func
    

class response:
    status_code: int
    description: str

    def __init__(
        self,
        status_code: int,
        description: str
    ) -> None:
        self.description = description
        self.status_code = status_code

    def __call__(
        self,
        func: Callable[..., T]
    ) -> Callable[..., T]:
        if not hasattr(func, 'responses'):
            func.responses = {} # type: ignore
        func.responses[self.status_code] = { # type: ignore
            k: v for k, v in self.__dict__.items()
            if v is not None and k != 'status_code'
        }
        return func