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
from typing import Coroutine

import fastapi
import fastapi.exceptions
import fastapi.routing

from cbra.types import Request


class APIRoute(fastapi.routing.APIRoute):

    def get_route_handler(
        self
    ) -> Callable[[fastapi.Request], Coroutine[Any, Any, fastapi.Response]]:
        super_handler = super().get_route_handler()

        async def handler(request: fastapi.Request) -> fastapi.Response:
            return await super_handler(
                Request(request.scope, request.receive)
            )

        return handler