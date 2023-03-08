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
    'test_send_message'
]


@pytest.mark.asyncio
async def test_send_message(
    request_factory: Callable[..., Coroutine[Any, Any, webhooks.WebhookResponse]]
):
    result = await request_factory(
        topic='hello',
        msg={'foo': 1},
        url='/'
    )
    assert result.success
    assert result.accepted