# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra


class AuthenticationRequiredEndpoint(cbra.Endpoint):
    require_authentication: bool = True
    async def head(self): assert False
    async def get(self): assert False
    async def put(self): assert False
    async def post(self): assert False
    async def patch(self): assert False
    async def delete(self): assert False
    async def trace(self): assert False


@pytest_asyncio.fixture # type: ignore
async def client():
    app = cbra.Application()
    AuthenticationRequiredEndpoint.add_to_router(app, path='/')
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client


@pytest.mark.parametrize("method", [
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "TRACE"
])
@pytest.mark.asyncio
async def test_require_authentication(
    client: httpx.Client,
    method: str
):
    response = await client.request(
        method=method,
        url='/',
    )
    assert response.status_code == 401