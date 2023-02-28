# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64
import datetime

import aorta
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra
from cbra.ext.google import AortaEndpoint
from cbra.ext.google import MessagePublished



AortaEndpoint: type[AortaEndpoint] = AortaEndpoint.configure( # type: ignore
    {'require_authentication': False}
)


@pytest.fixture
def app() -> cbra.Application:
    return cbra.Application()


@pytest_asyncio.fixture # type: ignore
async def client(app: cbra.Application):
    async with httpx.Client(base_url='http://cbra.ext.google', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_accept_message(
    app: cbra.Application,
    client: httpx.Client,
):
    app.add(AortaEndpoint)

    event = GoogleEvent(foo=1)
    envelope = event.envelope()
    message = MessagePublished.parse_obj({
        'subscription': 'projects/myproject/subscriptions/mysub',
        'message': {
            'messageId': 1,
            'publishTime': datetime.datetime.now().isoformat(),
            'data': base64.b64encode(bytes(envelope))
        }
    })
    response = await client.post(
        url='/',
        content=message.json(by_alias=True)
    )
    assert response.status_code == 202, response.content
    raise Exception

class GoogleEvent(aorta.Event):
    foo: int


class GoogleEventListener(aorta.EventListener):
    dep = cbra.inject('Missing')

    async def handle(self, event: GoogleEvent) -> int:
        return event.foo
    

aorta.register(GoogleEventListener)