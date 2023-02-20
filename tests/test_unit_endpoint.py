# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra


class MockEndpoint(cbra.Endpoint):

    async def head(self) -> dict[str, Any]:
        return {'method': self.request.method}

    async def get(self) -> dict[str, Any]:
        return {'method': self.request.method}

    async def post(self) -> dict[str, Any]:
        return {'method': self.request.method}

    async def put(self) -> dict[str, Any]:
        return {'method': self.request.method}

    async def patch(self) -> dict[str, Any]:
        return {'method': self.request.method}

    async def delete(self) -> dict[str, Any]:
        return {'method': self.request.method}


@pytest_asyncio.fixture # type: ignore
async def client():
    app = cbra.Application()
    MockEndpoint.add_to_router(app, path='/')
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client


@pytest.mark.parametrize("method", [
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
])
@pytest.mark.asyncio
async def test_basic_request_methods(
    client: httpx.Client,
    method: str
):
    response = await client.request(
        method=method,
        url='/',
    )
    assert response.status_code == 200
    if method != 'HEAD':
        assert response.headers.get('Content-Type') == 'application/json'
        dto = await response.json()
        assert dto.get('method') == method


@pytest.mark.parametrize("method", [
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"
])
@pytest.mark.asyncio
async def test_options(
    client: httpx.Client,
    method: str
):
    response = await client.options(url='/')
    assert response.allows(method)