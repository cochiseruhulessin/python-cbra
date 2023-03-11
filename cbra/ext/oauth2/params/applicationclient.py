# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncIterable

import fastapi
from headless.ext.oauth2 import Client

from cbra.core.conf import settings


__all__: list[str] = ['ApplicationClient']


async def get() -> AsyncIterable[Client]:
    params: dict[str, Any] = {
        'issuer': settings.APP_ISSUER,
        'client_id': settings.APP_CLIENT_ID,
        'client_secret': settings.APP_CLIENT_SECRET
    }
    async with Client(**params) as client:
        yield client


ApplicationClient: Client = fastapi.Depends(get)