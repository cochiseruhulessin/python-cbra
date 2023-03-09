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

from cbra.ext import webhooks


__all__: list[str] = [
    'test_handler_exception',
    'test_send_message',
    'test_unknown_format'
]


@pytest.mark.asyncio
async def test_send_message(
    request_factory: Callable[..., Coroutine[Any, Any, webhooks.WebhookResponse]],
    sign: bool
):
    result = await request_factory(
        topic='hello',
        msg={'foo': 1},
        url='/',
        sign=sign
    )
    assert result.success, result.reason
    assert result.accepted


@pytest.mark.asyncio
async def test_handler_exception(
    request_factory: Callable[..., Coroutine[Any, Any, webhooks.WebhookResponse]],
    sign: bool
):
    result = await request_factory(
        topic='exception',
        msg={'foo': 1},
        url='/',
        sign=sign
    )
    assert not result.success
    assert not result.accepted
    assert result.code == 'FATAL_EXCEPTION'


@pytest.mark.asyncio
async def test_unknown_format(
    request_factory: Callable[..., Coroutine[Any, Any, webhooks.WebhookResponse]],
    sign: bool
):
    result = await request_factory(
        topic='hello',
        msg={'_': 1},
        url='/',
        sign=sign
    )
    assert not result.success
    assert not result.accepted
    assert result.code == 'UNKNOWN_MESSAGE_FORMAT'