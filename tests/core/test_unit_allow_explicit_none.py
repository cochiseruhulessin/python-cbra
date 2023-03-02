# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Tests that a model field that is declared as optional is also allowed
on the response model.
"""
import pydantic
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra


class Model(cbra.ResourceModel):
    id: int = pydantic.Field(..., primary_key=True)
    value: str | None


class NoneResource(cbra.Resource, model=Model):

    async def retrieve(self, model_id: int) -> Model:
        return Model(id=1, value=None)


@pytest_asyncio.fixture(scope='session') # type: ignore
async def client():
    app = cbra.Application()
    app.add(NoneResource)
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client



@pytest.mark.asyncio
async def test_returns_200(
    client: httpx.Client
):
    response = await client.get(url='/models/1')
    assert response.status_code == 200, response.content