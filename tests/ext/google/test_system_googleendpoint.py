# Copyright (C) 2023 Cochise Ruhulessin
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
from cbra.ext.google import GoogleEndpoint


class GoogleServiceEndpoint(GoogleEndpoint):

    async def get(self) -> dict[str, Any]:
        return self.principal.dict()



@pytest_asyncio.fixture # type: ignore
async def client():
    app = cbra.Application()
    app.add(GoogleServiceEndpoint)
    async with httpx.Client(base_url='https://cbra.ext.google', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_basic_oidc_authentication_is_refused_without_token(
    client: httpx.Client,
    google_id_token: str
):
    response = await client.get(url='/')
    assert response.status_code == 401
    pass


@pytest.mark.asyncio
async def test_basic_oidc_authentication(
    client: httpx.Client,
    google_id_token: str
):
    response = await client.get(
        url='/',
        headers={'Authorization': f'Bearer {google_id_token}'}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_oidc_authentication_accepts_only_google(
    client: httpx.Client,
    google_id_token: str
):
    pass