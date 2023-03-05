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
from typing import TypeVar

import pydantic


T = TypeVar('T', bound='ModelMetadata')


class ModelMetadata(pydantic.BaseModel):
    created: datetime = pydantic.Field(
        default=...
    )

    deleted: datetime | None = pydantic.Field(
        default=None
    )

    generation: int = pydantic.Field(
        default=0,
    )

    uid: int | str | None = pydantic.Field(
        default=None
    )

    updated: datetime = pydantic.Field(
        default=...
    )

    @classmethod
    def initialize(cls: type[T]) -> T:
        now = datetime.now(timezone.utc)
        return cls.parse_obj({
            'created': now,
            'updated': now,
        })