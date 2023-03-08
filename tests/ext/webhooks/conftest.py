# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
import hmac
import json
from typing import Any
from typing import AsyncIterable
from typing import Callable
from typing import Coroutine
from typing import TypeAlias

import fastapi
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra
from cbra.ext import webhooks


RequestFactory: TypeAlias = Callable[[str, dict[str, Any]], Coroutine[Any, Any, webhooks.WebhookResponse]]
SECRET_KEY: bytes = b'test'


class BookWebhookEnvelope(webhooks.WebhookEnvelope):
    content: dict[str, Any]

    def __init__(
        self,
        content: dict[str, Any],
        topic: str = fastapi.Header(..., alias='X-Webhook-Topic'),
    ) -> None:
        self.content = content
        self.topic = topic


class BookWebhookEndpoint(webhooks.WebhookEndpoint):
    envelope: BookWebhookEnvelope
    domain: str = 'cbra.localhost'


class AuthenticatedBookWebhookEndpoint(BookWebhookEndpoint):
    pass


@pytest.fixture # type: ignore
def app() -> cbra.Application:
    app = cbra.Application()
    app.add(BookWebhookEndpoint, path='/')
    return app


@pytest.fixture
def secret_key() -> bytes:
    return SECRET_KEY


@pytest_asyncio.fixture # type: ignore
async def client(app: cbra.Application) -> AsyncIterable[httpx.Client]:
    params: dict[str, Any] = {
        'app': app,
        'base_url': "https://cbra"
    }
    async with httpx.Client(**params) as client:
        yield client


@pytest.fixture
def request_factory(
    client: httpx.Client,
    secret_key: bytes
) -> RequestFactory:
    async def f(* ,topic: str, msg: dict[str, Any], **kwargs: Any) -> webhooks.WebhookResponse:
        content = str.encode(json.dumps(msg), 'utf-8')
        digest = hmac.digest(
            secret_key,
            content,
            'sha256'
        )
        headers = kwargs.setdefault('headers', {})
        headers['Content-Type'] = "application/json"
        headers['X-Webhook-Topic'] = topic
        headers['X-Webhook-Signature'] = base64.b64encode(digest)
        response = await client.post(content=content, **kwargs)
        if response.status_code != 200:
            raise Exception(response.status_code, response.content)
        return webhooks.WebhookResponse.parse_obj(await response.json())
    return f # type: ignore
