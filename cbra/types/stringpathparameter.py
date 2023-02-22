# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .pathparameter import PathParameter
from .notfound import NotFound


class StringPathParameter(PathParameter):
    __module__: str = 'cbra.types'
    type: str = 'string'

    @classmethod
    def clean(cls, v: Any) -> str:
        try:
            return str(v)
        except (TypeError, ValueError):
            raise NotFound