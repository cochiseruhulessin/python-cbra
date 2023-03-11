# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Test that the redirect_uri is properly handled with a client that
has registered one URI.
"""
import urllib.parse

import pytest

from cbra.ext import oauth2
from .conftest import ServerClient
from .conftest import SUPPORTED_RESPONSE_TYPES


@pytest.mark.parametrize("response_type", SUPPORTED_RESPONSE_TYPES)
@pytest.mark.asyncio
async def test_not_allowed_redirect_uri_returns_400(
    client: ServerClient,
    authorization_endpoint: str,
    response_type: oauth2.types.ResponseType
):
    await client.login()
    params: dict[str, str] = {
        'client_id': 'app',
        'redirect_uri': 'https://www.google.com',
        'response_type': response_type.value
    }
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 403, dict(response.headers)
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'


@pytest.mark.parametrize("response_type", SUPPORTED_RESPONSE_TYPES)
@pytest.mark.parametrize("state", [None, "state"])
@pytest.mark.asyncio
async def test_redirect_uri_omitted_selects_default(
    client: ServerClient,
    authorization_endpoint: str,
    response_type: oauth2.types.ResponseType,
    state: str | None,
    issuer: str
):
    await client.login()
    params: dict[str, str] = {
        'client_id': 'app',
        'response_type': response_type.value
    }
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
    assert 'error' not in q
    assert 'iss' in q
    assert q['iss'] == issuer
    if state is not None:
        assert 'state' in q
        assert q['state'] == state