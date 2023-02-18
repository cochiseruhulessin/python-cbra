# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import Generator


class PathParameter:
    __module__: str = 'cbra.types'
    format: str | None = None
    type: str

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            type=cls.type,
            format=cls.format
        )

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., str | None], None, None]:
        yield cls.validate

    @classmethod
    def clean(cls, v: Any) -> Any:
        return v

    @classmethod
    def validate(cls, v: Any) -> str:
        # Called by FastAPI, must simply return the value.
        return v