# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import get_origin
from typing import Any
from typing import AsyncGenerator
from typing import TypeVar

from google.cloud.datastore import Client
from google.cloud.datastore import Entity
from google.cloud.datastore import Key
from google.cloud.datastore import Query

from cbra.core import ioc
from cbra.types import PersistedModel
from .runner import Runner


M = TypeVar('M', bound=PersistedModel)
Q = TypeVar('Q', bound=PersistedModel)
R = TypeVar('R')


class DatastoreRepository(Runner):
    __module__: str = 'cbra.ext.google'
    client: Client
    model: type[Any]

    def __init__(
        self,
        client: Client | Any = ioc.inject('GoogleDatastoreClient')
    ):
        if not isinstance(client, Client):
            raise TypeError(f"Invalid client: {repr(client)}")
        self.client = client

    async def allocate(self, model: type[Any], n: int = 1) -> list[int]:
        base = self.key(kind=model.__name__)
        return [
            x.id for x in
            await self.run_in_executor(
                functools.partial( # type: ignore
                    self.client.allocate_ids, # type: ignore
                    incomplete_key=base,
                    num_ids=n
                )
            )
        ]

    async def execute(self, query: Query, _R: type[R]) -> AsyncGenerator[R, None]:
        if _R == Key:
            query.keys_only()
        origin = get_origin(_R)
        for obj in await self.run_in_executor(query.fetch): # type: ignore
            if origin == int:
                yield obj.key.id
            elif origin in (Entity, dict):
                yield obj
            elif origin == Key:
                yield obj.key

    def key(
        self,
        kind: str | Any,
        entity_id: int | str | None = None,
        parent: Key | None = None
    ) -> Key:
        if not isinstance(kind, str):
            kind = kind.__name__
        assert isinstance(kind, str), repr(kind)
        key = self.client.key(kind, parent=parent) # type: ignore
        if isinstance(entity_id, (int, str)):
            key = self.client.key(kind, entity_id, parent=parent) # type: ignore
        return key

    async def get_entity_by_key(self, key: Key) -> Entity | None:
        return await self.run_in_executor(
            functools.partial(
                self.client.get, # type: ignore
                key=key
            )
        )

    async def get_model_by_key(
        self,
        model: type[M],
        key: int | str | Key
    ) -> M | None:
        if isinstance(key, (int, str)):
            key = self.key(model.__name__, key)
        assert isinstance(key, Key)
        entity = await self.get_entity_by_key(key)
        if entity is None:
            return None
        return self.restore(model, entity)

    async def one(self, model: type[Q], query: Query) -> Q | None:
        """Lookup exactly one object."""
        instance: Q | None = None
        for entity in await self.run_in_executor(query.fetch): # type: ignore
            if instance is not None:
                raise RuntimeError("Multiple objects returned.")
            instance = self.restore(model, entity)
        return instance

    async def put(self, instance: PersistedModel, exclude: set[str] | None = None) -> Key:
        Model: type[PersistedModel] = type(instance)
        exclude = set(exclude or set()) | {'__surrogate__'}
        field: str | None = None
        if instance.__surrogate__ != NotImplemented:
            field = Model.__surrogate__.attname # type: ignore

            assert field is not None
            if instance.__surrogate__ is None:
                setattr(instance, field, (await self.allocate(Model))[0])

            # Exclude the surrogate key since it is retained in the Google Datastore
            # entities' key.
            exclude.add(field)

        data = instance.dict(exclude=exclude)

        # Create the entity and persist it to the datastore.
        assert instance.__surrogate__ is not None
        entity = Entity(
            key=self.key(Model.__name__, instance.__surrogate__)
        )
        entity.update(data) # type: ignore
        await self.run_in_executor(self.client.put, entity) # type: ignore
        return entity.key # type: ignore

    def construct_key(self, model: Any) -> Key:
        raise NotImplementedError

    def query(self, kind: str | type[Q], ancestor: Key | None = None) -> Query:
        if not isinstance(kind, str):
            kind = kind.__name__
        return self.client.query(kind=kind, ancestor=ancestor) # type: ignore

    def restore(self, model: type[Q], entity: dict[str, Any] | Entity) -> Q:
        if model.__surrogate__ != NotImplemented: # type: ignore
            field_name = model.__surrogate__.attname # type: ignore
        return model.parse_obj({
            **entity,
            field_name: entity.key.id # type: ignore
        })