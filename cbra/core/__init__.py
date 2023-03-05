# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# type: ignore
import importlib
import inspect
import pathlib
import os
from typing import cast
from typing import Any
from typing import Callable
from typing import TypeVar

import aorta
import unimatrix.runtime
import yaml
from pydantic import Field

from .application import Application
from .endpoint import Endpoint
from . import ioc
from .localmessagetransport import LocalMessageTransport
from .messagepublisher import MessagePublisher
from .messagerunner import MessageRunner
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
from .resource import Versioned
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
    'LocalMessageTransport',
    'MessagePublisher',
    'MessageRunner',
    'Mutable',
    'QueryResult',
    'Replace',
    'Resource',
    'ResourceModel',
    'ResourceType',
    'Retrieve',
    'SecretKey',
    'Update',
    'Versioned',
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
    

def autodiscover(
    qualname: str, cls: type[T] | None  = None
) -> T:
    os.environ.setdefault(
        'PYTHON_SETTINGS_MODULE',
        unimatrix.runtime.get_settings_module(__name__)
    )
    parent = qualname.rsplit('.', 1)[0]
    modules: list[str] = [
        'endpoints',
        'handlers',
        'listeners',
        'resources',
    ]
    asgi = importlib.import_module(qualname)
    params: dict[str, Any] = {
        'docs_url'  : '/ui',
        'redoc_url' : '/'
    }
    base = pathlib.Path(asgi.__file__).parent
    meta = base.joinpath('asgi.yml')
    if meta.exists():
        params.update(yaml.safe_load(meta.read_text()))
    cls = cls or Application
    app = cast(Application, cls(**params))
    addables: tuple[type] = (
        Resource,
        aorta.CommandHandler,
        aorta.Sewer,
        aorta.EventListener,
    )
    for name in modules:
        try:
            module = importlib.import_module(f'{parent}.{name}')
        except ImportError:
            # Raise the error if the module exists because then it
            # was something in the module that raised it.
            if any([
                base.joinpath(name).exists(),
                base.joinpath(f'{name}.py').exists()
            ]):
                raise
            continue
        for _, member in inspect.getmembers(module):
            if not inspect.isclass(member) or not issubclass(member, addables):
                continue
            app.add(member)

    return app