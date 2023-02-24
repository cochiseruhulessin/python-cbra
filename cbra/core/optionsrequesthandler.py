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

from cbra.types import IEndpoint
from .requesthandler import RequestHandler


class OptionsRequestHandler(RequestHandler[IEndpoint]):
    include_in_schema: bool = True

    def __init__(
        self,
        name: str,
        include_in_schema: bool | None = None
    ):
        super().__init__(
            name=name,
            method='OPTIONS',
            func=self.handle
        )

    def clone(self):
        return type(self)(self._endpoint_name, self.include_in_schema)

    async def handle(
        self,
        endpoint: IEndpoint,
        *args: Any,
        **kwargs: Any
    ) -> fastapi.Response:
        return fastapi.Response(
            status_code=200,
            headers={
                'Allow': str.join(',', endpoint.allowed_http_methods)
            }
        )