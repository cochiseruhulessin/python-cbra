# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#import functools
#from typing import Any
#from typing import TypeVar
#
#from google.cloud.datastore import Client
#from google.cloud.datastore import Entity
#from google.cloud.datastore import Key
#
#from cbra.core import ioc
#from cbra.types import IRepository
#from .datastorecursor import DatastoreCursor
#from .datastorestate import DatastoreState
#from .runner import Runner
#
#import pydantic
#
#
#M = TypeVar('M', bound=pydantic.BaseModel)
#P = TypeVar('P', bound=pydantic.BaseModel)
#
#
#class DatastoreRepository(IRepository[DatastoreCursor], Runner):
#    __module__: str = 'cbra.ext.google'
#    client: Client
#    cursor_class = DatastoreCursor
#    storage_model: type[DatastoreState] = DatastoreState
#
#    def __init__(
#        self,
#        client: Client | Any = ioc.inject('GoogleDatastoreClient')
#    ):
#        if not isinstance(client, Client):
#            raise TypeError(f"Invalid client: {repr(client)}")
#        self.client = client
#
#    def storage_key(
#        self,
#        model: type,
#        id: int | str | None = None,
#        parent: Key | None = None
#    ) -> Key:
#        kind = model.__name__
#        key = self.client.key(kind, parent=parent) # type: ignore
#        if id is not None:
#            key = self.client.key(kind, id, parent) # type: ignore
#        return key
#
#    async def load(self, model: type[P], resource_id: Any) -> DatastoreState | None:
#        assert isinstance(id, int) or id is None # nosec
#        obj = None
#        entity = await self.get_entity_by_id(resource_id, model)
#        if entity is not None:
#            obj = self.storage_model.parse_obj(entity)
#        return obj
#
#    async def get_entity_by_id(
#        self,
#        entity_id: int,
#        model: type,
#        parent: Key | None = None
#    ) -> Entity | None:
#        return await self.run_in_executor(
#            functools.partial(
#                self.client.get, # type: ignore
#                key=self.storage_key(
#                    model=model,
#                    id=entity_id,
#                    parent=parent
#                )
#            )
#        )