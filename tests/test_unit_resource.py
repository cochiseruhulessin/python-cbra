# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra
from cbra.core.resource.test import Book
from cbra.core.resource.test import BookResource


@pytest_asyncio.fixture(scope='session') # type: ignore
async def client():
    app = cbra.Application()
    BookResource.add_to_router(app, path='/')
    async with httpx.Client(base_url='https://cbra', app=app) as client:
        yield client


@pytest_asyncio.fixture # type: ignore
async def book(client: httpx.Client):
    response = await client.post(
        url='/books',
        json={
            'title': f"Foo {os.urandom(10).hex()}",
            'publications': []
        }
    )
    assert response.status_code == 201
    resource = Book.parse_obj(await response.json())
    yield resource
    response = await client.delete(url=f'/books{resource.id}', allow_none=True)
    assert response.status_code in {200, 404}


@pytest.mark.asyncio
async def test_get(
    client: httpx.Client
):
    response = await client.get(url='/books/1')
    resource = Book.parse_obj(await response.json())
    assert resource.id == 1


@pytest.mark.asyncio
async def test_post(
    client: httpx.Client
):
    response = await client.post(
        url='/books',
        json={
            'title': "Foo",
            'publications': []
        }
    )
    resource = Book.parse_obj(await response.json())
    assert resource.id != 1


@pytest.mark.asyncio
async def test_delete(
    client: httpx.Client,
    book: Book
):
    response = await client.delete(url=f'/books/{book.id}')
    assert response.status_code == 200

    response = await client.get(url=f'/books/{book.id}', allow_none=True)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update(
    client: httpx.Client,
    book: Book
):
    title = f'Foo {os.urandom(10).hex()}'
    response = await client.request(
        method='PATCH',
        url=f'/books/{book.id}',
        json={'title': title}
    )
    assert response.status_code == 200
    new = Book.parse_obj(await response.json())
    assert new.id == book.id
    assert new.title == title


@pytest.mark.asyncio
async def test_replace(
    client: httpx.Client,
    book: Book
):
    title = f'Foo {os.urandom(10).hex()}'

    # Must be full Book resource.
    response = await client.request(
        method='PUT',
        url=f'/books/{book.id}',
        json={'title': title}
    )
    assert response.status_code == 422

    response = await client.request(
        method='PUT',
        url=f'/books/{book.id}',
        json={**book.dict(), 'title': title}
    )
    assert response.status_code == 200
    new = Book.parse_obj(await response.json())
    assert new.id == book.id
    assert new.title == title