# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Tests that a model field that is declared as optional is also allowed
on the response model.
"""
from typing import Any

import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra


class Endpoint(cbra.Endpoint):
    versioned: bool = True
    test: bool = True

    async def post(self, data: dict[str, Any]) -> None:
        assert set(data.get('If-Match') or []) == self.etag


@pytest_asyncio.fixture(scope='session') # type: ignore
async def client():
    app = cbra.Application()
    app.add(Endpoint, path='/')
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_etag_single_value(
    client: httpx.Client
):
    response = await client.post(
        url='/',
        headers={'If-Match': 'foo'},
        json={'If-Match': ['foo']}
    )
    assert 200 <= response.status_code < 300, response.content


@pytest.mark.asyncio
async def test_etag_multiple_value(
    client: httpx.Client
):
    response = await client.post(
        url='/',
        headers={'If-Match': 'foo,bar'},
        json={'If-Match': ['foo', 'bar']}
    )
    assert 200 <= response.status_code < 300, response.content