# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import pytest
from headless.core import httpx


@pytest.mark.parametrize("state", [
    None,
    'state'
])
@pytest.mark.asyncio
async def test_missing_response_type_returns_303_error(
    client: httpx.Client,
    authorization_endpoint: str,
    state: str | None,
    issuer: str
):
    params: dict[str, str] = {'client_id': 'app', 'response_type': 'foo'}
    if state is not None:
        params['state'] = state
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 303, response.content
    assert 'Location' in response.headers
    p = urllib.parse.urlparse(response.headers['Location'])
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'error' in q
    assert q['error'] == "invalid_request"
    assert 'iss' in q
    assert q['iss'] == issuer
    if state is not None:
        assert 'state' in q
        assert q['state'] == state


@pytest.mark.parametrize("state", [
    None,
    'state'
])
@pytest.mark.asyncio
async def test_invalid_response_type_returns_303_error(
    client: httpx.Client,
    authorization_endpoint: str,
    state: str | None,
    issuer: str
):
    params: dict[str, str] = {'client_id': 'app', 'response_type': 'foo'}
    if state is not None:
        params['state'] = state
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 303, response.content
    assert 'Location' in response.headers
    p = urllib.parse.urlparse(response.headers['Location'])
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'error' in q
    assert 'iss' in q
    assert q['iss'] == issuer
    assert q['error'] == "invalid_request"
    if state is not None:
        assert 'state' in q
        assert q['state'] == state