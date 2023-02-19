# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import fastapi
import uvicorn

import cbra


class Book(cbra.ResourceModel):
    id: int | None = cbra.Field(
        default=None,
        read_only=True
    )
    title: str
    published: datetime.date

    class Config:
        title: str = 'Foo'


class BookResource(cbra.Resource, model=Book):

    async def create(self, resource: Book):
        resource.id = 1
        return resource

    async def destroy(self, book_id: int):
        pass

    async def list(self):
        pass

    async def retrieve(self, book_id: int) -> None:
        return Book(id=book_id, title="Foo", published=datetime.date.today())

    async def replace(self, book_id: int, resource: Book):
        pass

    async def update(self, book_id: int, resource: Book):
        pass


app = fastapi.FastAPI(docs_url='/ui')
BookResource.add_to_router(app, path='/')

if __name__ == '__main__':
    uvicorn.run('__main__:app', reload=True) # type: ignore
