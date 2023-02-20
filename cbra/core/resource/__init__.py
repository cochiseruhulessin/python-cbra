# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .create import Create
from .delete import Delete
from .replace import Replace
from .resource import Resource
from .resourcemodel import ResourceModel
from .resourcetype import ResourceType
from .retrieve import Retrieve
from .update import Update


__all__: list[str] = [
    'Create',
    'Delete',
    'Mutable',
    'Replace',
    'Resource',
    'ResourceModel',
    'ResourceType',
    'Retrieve',
    'Update',
]


class Mutable(
    Create,
    Delete,
    Replace,
    Retrieve,
    Update,
):
    __module__: str = 'cbra.core'