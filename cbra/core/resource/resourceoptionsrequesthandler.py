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

from ..requesthandler import RequestHandler
from .iresource import IResource


class ResourceOptionsRequestHandler(RequestHandler[IResource]): # type: ignore
    allow: set[str]
    include_in_schema: bool = False

    def __init__(
        self,
        name: str,
        allow: set[str],
        include_in_schema: bool | None = True
    ):
        self.allow = allow
        super().__init__(
            name=name,
            method='OPTIONS',
            func=self.handle
        )

    async def handle(
        self,
        endpoint: IResource,
        *args: Any,
        **kwargs: Any
    ) -> fastapi.Response:
        return fastapi.Response(
            status_code=200,
            headers={
                'Allow': str.join(',', self.allow)
            }
        )