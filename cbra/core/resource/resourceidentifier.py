# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

import pydantic
import fastapi


T = TypeVar('T', bound='ResourceIdentifier')


class ResourceIdentifier(pydantic.BaseModel):

    @classmethod
    def depends(cls: type[T]) -> None | T:
        return fastapi.Depends(cls.frompath)

    @classmethod
    def frompath(
        cls: type[T],
        request: fastapi.Request
    ) -> None | T:
        try:
            return cls.parse_obj(request.path_params)
        except pydantic.ValidationError:
            return None