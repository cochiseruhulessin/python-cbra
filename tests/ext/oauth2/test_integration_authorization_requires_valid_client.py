# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
from headless.core import httpx


@pytest.mark.asyncio
async def test_missing_client_id_returns_400(
    client: httpx.Client,
    authorization_endpoint: str
):
    response = await client.get(
        url=authorization_endpoint,
        params={}
    )
    assert response.status_code == 400, response.content
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'


@pytest.mark.asyncio
async def test_invalid_client_id_returns_400(
    client: httpx.Client,
    authorization_endpoint: str,
    random_id: str
):
    response = await client.get(
        url=authorization_endpoint,
        params={'client_id': random_id}
    )
    assert response.status_code == 400, response.content
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'