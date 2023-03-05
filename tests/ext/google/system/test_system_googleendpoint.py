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
from cbra.types import JSONWebTokenPrincipal


class GoogleServiceEndpoint(GoogleEndpoint):

    async def get(self) -> dict[str, Any]:
        return self.principal.dict()


@pytest.fixture
def app() -> cbra.Application:
    return cbra.Application()


@pytest_asyncio.fixture # type: ignore
async def client(app: cbra.Application):
    async with httpx.Client(base_url='http://cbra.ext.google', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_basic_oidc_authentication_is_refused_without_token(
    app: cbra.Application,
    client: httpx.Client,
    google_id_token: str
):
    app.add(GoogleServiceEndpoint)
    response = await client.get(url='/')
    assert response.status_code == 401
    pass


@pytest.mark.asyncio
async def test_basic_oidc_authentication(
    app: cbra.Application,
    client: httpx.Client,
    google_id_token: str
): 
    claims: dict[str, Any] = JSONWebTokenPrincipal.parse_jwt(google_id_token)
    app.add(GoogleServiceEndpoint.configure({'allowed_service_accounts': {claims['email']}})) # type: ignore
    response = await client.get(
        url='/',
        headers={'Authorization': f'Bearer {google_id_token}'}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_basic_oidc_authentication_accepts_only_whitelisted(
    app: cbra.Application,
    client: httpx.Client,
    google_id_token: str
): 
    app.add(GoogleServiceEndpoint.configure({'allowed_service_accounts': set()})) # type: ignore
    response = await client.get(
        url='/',
        headers={'Authorization': f'Bearer {google_id_token}'}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_basic_oidc_authentication_accepts_only_google(
    app: cbra.Application,
    client: httpx.Client,
    google_id_token: str
):
    pytest.skip("TODO")