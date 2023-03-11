# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any

from google.cloud.datastore import Client

from .runner import Runner
from .types import IDatastoreCursor
from .types import IDatastoreEntity
from .types import IDatastoreKey
from .types import IDatastoreQuery


class BaseDatastoreRepository(Runner):
    __module__: str = 'cbra.ext.google'

    def __init__(
        self,
        client: Client
    ) -> None:
        self.client = client

    async def allocate(self, name: str) -> int:
        base = self.key(kind=name)
        result = await self.run_in_executor(
            functools.partial( # type: ignore
                self.client.allocate_ids, # type: ignore
                incomplete_key=base,
                num_ids=1
            )
        )
        return [x for x in result][0].id

    def key(
        self,
        kind: str,
        identifier: int | str | None = None,
        parent: IDatastoreKey | None = None
    ) -> IDatastoreKey:
        args: list[Any] = [kind]
        if identifier is not None:
            args.append(identifier)
        return self.client.key(*args, parent=parent) # type: ignore

    def entity_factory(self, key: IDatastoreKey) -> IDatastoreEntity:
        return self.client.entity(key) # type: ignore

    def entity(
        self,
        kind: str,
        key: int | str | IDatastoreKey | None = None,
        parent: IDatastoreKey | None = None
    ) -> IDatastoreEntity:
        if isinstance(key, (int, str)):
            key = self.key(kind, key)
        return self.client.entity(key or self.key(kind, parent=parent)) # type: ignore

    def query(self, *args: Any, **kwargs: Any) -> IDatastoreQuery:
        return self.client.query(*args, **kwargs) # type: ignore

    async def execute(self, query: IDatastoreQuery, **kwargs: Any) -> IDatastoreCursor:
        cursor = await self.run_in_executor(functools.partial(query.fetch, **kwargs))
        return cursor

    async def get_entity_by_key(self, key: IDatastoreKey) -> IDatastoreEntity | None:
        return await self.run_in_executor(
            functools.partial(
                self.client.get, # type: ignore
                key=key
            )
        )
    
    async def first(self, query: IDatastoreQuery) -> IDatastoreEntity | None:
        """Return the first object in the query, or none."""
        for entity in await self.execute(query, limit=1):
            return entity

    async def put(self, entity: IDatastoreEntity) -> IDatastoreKey:
        await self.run_in_executor(self.client.put, entity) # type: ignore
        return entity.key # type: ignore