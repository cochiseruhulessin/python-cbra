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
import collections

import pydantic
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra


QueryResult = collections.namedtuple('QueryResult', ['token', 'items'])


class AliasModel(cbra.ResourceModel):
    id: int = pydantic.Field(..., primary_key=True)
    value: str | None = pydantic.Field(..., alias='aliasedValue')


class AliasedResource(cbra.Resource, cbra.Collection, model=AliasModel):
    response_model_by_alias: bool = True

    async def retrieve(self, aliasmodel_id: int) -> AliasModel:
        return AliasModel(id=1, aliasedValue=None)

    async def filter(self, *args):
        return QueryResult('', [AliasModel(id=1, aliasedValue=None)])


@pytest_asyncio.fixture(scope='session') # type: ignore
async def client():
    app = cbra.Application()
    app.add(AliasedResource)
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_retrieve_response_model_with_aliases(
    client: httpx.Client
):
    response = await client.get(url='/aliasmodels/1')
    assert response.status_code == 200, response.content


@pytest.mark.asyncio
async def test_list_response_model_with_aliases(
    client: httpx.Client
):
    response = await client.get(url='/aliasmodels')
    assert response.status_code == 200, response.content