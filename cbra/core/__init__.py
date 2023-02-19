# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any

from pydantic import Field

from .application import Application
from .endpoint import Endpoint
from .resource import *

from unimatrix.conf import settings # type: ignore


settings: Any = cast(Any, settings)


__all__: list[str] = [
    'settings',
    'Application',
    'Create',
    'Delete',
    'Endpoint',
    'Field',
    'Replace',
    'Resource',
    'ResourceModel',
    'ResourceType',
    'Retrieve',
    'Update'
]