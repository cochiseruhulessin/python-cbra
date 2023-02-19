# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import secrets

import cbra.core as cbra
from .book import Book
from .bookpublication import BookPublication


class BookResource(
    cbra.Resource,
    cbra.Create,
    cbra.Delete,
    cbra.Replace,
    cbra.Retrieve,
    cbra.Update,
    model=Book
):
    books: dict[int, Book] = {
        1: Book(
            id=1,
            title="The Hitchhiker's Guide to the Galaxy",
            publications=[
                BookPublication(country_code='UK', published=datetime.date(1979, 10, 12)),
                BookPublication(country_code='US', published=datetime.date(1980, 10, 1)),
            ]
        )
    }

    async def can_create(self, resource: Book) -> bool:
        return not any([x.title == resource.title for x in self.books.values()])

    async def delete(self, resource: Book):
        assert resource.id is not None
        self.books.pop(resource.id)

    async def get_object(self) -> Book | None:
        return self.books.get(int(self.request.path_params['book_id']))

    async def persist(self, resource: Book, create: bool = False) -> Book:
        if create:
            assert resource.id is None
            resource.id = secrets.choice(range(1000, 9999))
        assert resource.id is not None
        self.books[resource.id] = resource
        return resource