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
from typing import TypeVar

from pydantic.validators import str_validator


T = TypeVar('T', bound='ETagSet')


class ETagSet(str):
    __module__: str = 'cbra.types'
    openapi_format: str = 'comma-separated'
    openapi_type: str = 'string'

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            type=cls.openapi_format,
            format=cls.openapi_format
        )

    @classmethod
    def __get_validators__(cls: type[T]) -> Generator[Callable[..., str | T], None, None]:
        yield str_validator

    def toset(self) -> set[str]:
        return set(filter(bool, [str.strip(x) for x in self.split(',')]))