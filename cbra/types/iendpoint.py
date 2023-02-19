# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi

from .iroutable import IRoutable


class IEndpoint:
    __module__: str = 'cbra.types'
    allowed_http_methods: list[str]
    handlers: list[IRoutable]
    include_in_schema: bool = True
    request: fastapi.Request
    response: fastapi.Response
    router: fastapi.APIRouter

    def get_success_headers(self, data: Any) -> dict[str, Any]:
        """Return a mapping holding the headers to add on a successful
        request based on the return value of the request handler.
        """
        return {}