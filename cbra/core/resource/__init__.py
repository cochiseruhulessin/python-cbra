# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .create import Create
from .collection import Collection
from .delete import Delete
from .queryresult import QueryResult
from .replace import Replace
from .resource import Resource
from .resourcemodel import ResourceModel
from .resourceprotocol import ResourceProtocol
from .resourcetype import ResourceType
from .retrieve import Retrieve
from .update import Update
from .versioned import Versioned


__all__: list[str] = [
    'Create',
    'Collection',
    'Delete',
    'Mutable',
    'QueryResult',
    'Replace',
    'Resource',
    'ResourceModel',
    'ResourceProtocol',
    'ResourceType',
    'Retrieve',
    'Update',
    'Versioned',
]


class Mutable(
    Create,
    Delete,
    Replace,
    Retrieve,
    Update,
):
    __module__: str = 'cbra.core'