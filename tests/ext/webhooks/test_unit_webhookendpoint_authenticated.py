# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import Coroutine

import pytest

import cbra.core as cbra
from cbra.ext import webhooks
from .base import *
from .conftest import AuthenticatedBookWebhookEndpoint


@pytest.fixture # type: ignore
def app() -> cbra.Application:
    app = cbra.Application()
    app.add(AuthenticatedBookWebhookEndpoint, path='/')
    return app


@pytest.fixture
def sign() -> bool:
    return True


@pytest.mark.asyncio
async def test_send_message_unsigned(
    request_factory: Callable[..., Coroutine[Any, Any, webhooks.WebhookResponse]]
):
    result = await request_factory(
        topic='hello',
        msg={'foo': 1},
        url='/',
        sign=False
    )
    assert not result.success
    assert result.code == 'INVALID_SIGNATURE'