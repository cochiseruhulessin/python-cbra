# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hmac
from typing import Any

import pytest
import pytest_asyncio
from ckms.utils import b64encode_str
from headless.core import httpx

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.types import Session


async def sign_hmac(value: bytes) -> str:
    return b64encode_str(hmac.digest(b'foo', value, 'sha384'))


def test_set_clears_hmac():
    session = Session.new()
    session.hmac = 'foo'
    session.set('sub', 'bar')
    assert session.hmac is None


def test_set_returns_modified():
    session = Session.new()
    assert session.set('sub', 'bar')
    assert not session.set('sub', 'bar')


# TODO: move to other file
@pytest.mark.asyncio
async def test_no_session_without_modify_sets_session(
    client: httpx.Client
):
    response = await client.get(url='/')
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies


@pytest.mark.asyncio
async def test_session_updates_are_returned(
    client: httpx.Client
):
    response = await client.post(url='/')
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    obj = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert obj is not None
    assert obj.claims is not None
    assert obj.claims.iss == 'foo'
    assert obj.claims.sub == 'bar'


@pytest.mark.asyncio
async def test_session_invalid_key_is_rotated(
    client: httpx.Client
):
    response = await client.post(url='/')
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    obj = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert obj is not None
    print(f"Estblished session with HMAC {obj.hmac}")

    sig = obj.hmac
    evil = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert evil is not None
    evil.set('sub', 'baz')
    await evil.sign(sign_hmac)
    assert evil.hmac != sig
    assert evil.as_cookie() != obj.as_cookie()
    print(f"Attacker created session with HMAC {evil.hmac}")

    # The original session must validate
    response = await client.get(
        url='/',
        cookies={settings.SESSION_COOKIE_NAME: response.impl.cookies[settings.SESSION_COOKIE_NAME]}
    )
    assert settings.SESSION_COOKIE_NAME not in response.impl.cookies

    # The tampered session rotates to a new session
    print("Sending evil session")
    client.cookies.clear()
    response = await client.get(
        url='/',
        cookies={settings.SESSION_COOKIE_NAME: evil.as_cookie()}
    )
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    session = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert session is not None
    assert session.id != evil.id


@pytest.mark.asyncio
async def test_session_clear(
    client: httpx.Client
):
    response = await client.post(url='/')
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    session1 = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert session1 is not None

    response = await client.delete(url='/')
    assert settings.SESSION_COOKIE_NAME in response.impl.cookies
    session2 = Session.parse_cookie(response.impl.cookies[settings.SESSION_COOKIE_NAME])
    assert session2 is not None
    assert session1.id != session2.id


class SessionEndpoint(cbra.Endpoint):

    async def get(self) -> dict[str, Any]:
        await self.session
        return self.session.data.dict()

    async def post(self) -> dict[str, Any]:
        await self.session
        self.session.set('iss', 'foo')
        self.session.set('sub', 'bar')
        return self.session.data.dict()

    async def delete(self) -> dict[str, Any]:
        await self.session
        await self.session.clear()
        return self.session.data.dict()


@pytest_asyncio.fixture # type: ignore
async def client():
    app = cbra.Application()
    app.add(SessionEndpoint)
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client