# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone
from typing import Any

import pydantic

from cbra.types import IResourceState


now = lambda: datetime.now(timezone.utc)


class ResourceMetadata(pydantic.BaseModel, IResourceState[Any]):
    created: datetime = pydantic.Field(default_factory=now)
    updated: datetime | None = pydantic.Field(default=None)
    deleted: datetime | None = pydantic.Field(default=None)
    version: str = pydantic.Field(default='')
    generation: int = pydantic.Field(default=0)