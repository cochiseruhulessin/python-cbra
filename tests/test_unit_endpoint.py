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


class AnnotationEndpoint(cbra.Endpoint):

    async def post(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            'method': self.request.method,
            'headers': {str.lower(k): v for k, v in self.request.headers.items()},
            'data': data
        }


@pytest_asyncio.fixture # type: ignore
async def client():
    app = cbra.Application()
    app.add(MockEndpoint, path='/')
    app.add(AnnotationEndpoint, path='/annotations')

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


# Test that a function can use f(body_json: dict[str, Any])
@pytest.mark.asyncio
async def test_dict_from_json_without_content_type(
    client: httpx.Client
):
    response = await client.post(url='/annotations', content='{"foo": 1}')
    assert response.status_code == 200
    result = await response.json()
    assert 'data' in result
    assert 'headers' in result
    assert 'content-type' not in result['headers']
    assert 'foo' in result['data']


@pytest.mark.asyncio
async def test_dict_from_json_with_content_type(
    client: httpx.Client
):
    response = await client.post(
        url='/annotations',
        content='{"foo": 1}',
        headers={'Content-Type': "application/json"}
    )
    assert response.status_code == 200
    result = await response.json()
    assert 'data' in result
    assert 'headers' in result
    assert 'content-type' in result['headers']
    assert 'foo' in result['data']


@pytest.mark.asyncio
async def test_dict_from_invalid_json(
    client: httpx.Client
):
    response = await client.post(url='/annotations', content='{"foo"}: 1}')
    assert response.status_code == 422