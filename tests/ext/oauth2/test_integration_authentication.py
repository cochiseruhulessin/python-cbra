# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Test that the authorization endpoint properly authenticates the
subject.
"""
import urllib.parse

import pytest
from headless.core import httpx

from cbra.core.conf import settings
from cbra.ext import oauth2
from .conftest import SUPPORTED_RESPONSE_TYPES


@pytest.mark.parametrize("response_type", SUPPORTED_RESPONSE_TYPES)
@pytest.mark.asyncio
async def test_unauthenticated_redirects_to_login_endpoint(
    client: httpx.Client,
    authorization_endpoint: str,
    response_type: oauth2.types.ResponseType
):
    params: dict[str, str] = {
        'client_id': 'app',
        'redirect_uri': 'https://www.google.com',
        'response_type': response_type.value
    }
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 303, response.content
    assert 'Location' in response.headers
    p = urllib.parse.urlparse(response.headers['Location'])
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'next' in q, q
    assert 'request' in q, q


@pytest.mark.parametrize("response_type", SUPPORTED_RESPONSE_TYPES)
@pytest.mark.asyncio
async def test_unauthenticated_without_session_gets_session(
    client: httpx.Client,
    authorization_endpoint: str,
    response_type: oauth2.types.ResponseType
):
    params: dict[str, str] = {
        'client_id': 'app',
        'redirect_uri': 'https://www.google.com',
        'response_type': response_type.value
    }
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 303, response.content
    assert 'Set-Cookie' in response.headers
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    p = urllib.parse.urlparse(response.headers['Location'])
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'next' in q
    assert 'request' in q


@pytest.mark.parametrize("response_type", SUPPORTED_RESPONSE_TYPES)
@pytest.mark.asyncio
async def test_evil_session_gets_new_session(
    evil_client: httpx.Client,
    authorization_endpoint: str,
    response_type: oauth2.types.ResponseType
):
    client = evil_client
    params: dict[str, str] = {
        'client_id': 'app',
        'redirect_uri': 'https://www.google.com',
        'response_type': response_type.value
    }
    response = await client.get(
        url=authorization_endpoint,
        params=params
    )
    assert response.status_code == 303, response.content
    assert 'Location' in response.headers
    p = urllib.parse.urlparse(response.headers['Location'])
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'next' in q
    assert 'request' in q

    assert 'Set-Cookie' in response.headers
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies