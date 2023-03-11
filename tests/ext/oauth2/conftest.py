# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone 
from typing import Any
from typing import AsyncIterable

import pytest
import pytest_asyncio
from ckms.core import Keychain
from headless.core import httpx
from headless.ext.oauth2 import Client

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.core.iam.models import Subject
from cbra.types import Session
from cbra.ext import oauth2


SUPPORTED_RESPONSE_TYPES: list[oauth2.types.ResponseType] = [
    oauth2.types.ResponseType.code
]


class ServerClient(httpx.Client):

    async def login(self, sub: int = 1) -> None:
        key = await cbra.SecretKey.setup()
        session = Session.new()
        session.update({
            'iss': 'https://cbra',
            'sub': sub
        })
        await session.sign(key.sign)
        self.cookies[settings.SESSION_COOKIE_NAME] = session.as_cookie()


@pytest.fixture # type: ignore
def app(issuer: str) -> cbra.Application:
    app = cbra.Application()
    app.add(
        oauth2.AuthorizationServer(
            iss=issuer,
            response_types=[
                oauth2.types.ResponseType.code
            ]
        )
    )
    return app


@pytest.fixture(scope='function')
def storage(
    app: cbra.Application
):
    impl = app.container.require('AuthorizationServerStorage')
    impl.resolve()
    yield impl.get()()


@pytest.fixture
def application_client() -> oauth2.models.Client:
    return oauth2.models.Client.parse_obj({
        'kind': 'Application',
        'client_id': 'app',
        'info': {
            'organization_name': "ACME",
            'display_name': "CBRA Test Client",
        },
        'allowed_redirect_uris': ["https://cbra/oauth2/callback"]
    })


@pytest_asyncio.fixture # type: ignore
async def idp(
    app: cbra.Application
) -> AsyncIterable[Client]:
    params: dict[str, Any] = {
        'app': app,
        'issuer': 'https://cbra'
    }
    async with Client(**params) as client:
        yield client


@pytest_asyncio.fixture # type: ignore
async def client(
    app: cbra.Application,
    storage: oauth2.types.IAuthorizationServerStorage,
    application_client: oauth2.models.Client,
    issuer: str
) -> AsyncIterable[ServerClient]:
    params: dict[str, Any] = {
        'app': app,
        'base_url': issuer
    }
    await storage.persist(application_client)
    async with ServerClient(**params) as client:
        yield client


@pytest_asyncio.fixture # type: ignore
async def evil_client(
    app: cbra.Application,
    storage: oauth2.types.IAuthorizationServerStorage,
    application_client: oauth2.models.Client,
    subject: Subject
) -> AsyncIterable[httpx.Client]:
    class EvilSecretKey(cbra.SecretKey):
        keychain: Keychain = Keychain()
    key = await EvilSecretKey.setup('evil')
    session = Session.new()
    await session.sign(key.sign)
    params: dict[str, Any] = {
        'app': app,
        'base_url': 'https://cbra',
        'cookies': {
            settings.SESSION_COOKIE_NAME: session.as_cookie()
        }
    }
    await storage.persist(application_client)
    await storage.persist(subject)
    async with httpx.Client(**params) as client:
        yield client


@pytest.fixture
def authorization_endpoint() -> str:
    return '/authorize'


@pytest.fixture
def issuer() -> str:
    return 'https://cbra'


@pytest.fixture
def subject() -> Subject:
    now = datetime.now(timezone.utc)
    return Subject(
        kind='User',
        uid=1,
        created=now,
        seen=now,
    )