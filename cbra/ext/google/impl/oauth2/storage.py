# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
from typing import Any
from typing import TypeVar


import pydantic
from google.cloud.datastore import Client

import cbra.core as cbra
from cbra.ext.google import BaseDatastoreRepository
from cbra.ext.google.types import IDatastoreEntity
from cbra.ext.google.types import IDatastoreKey
from cbra.ext.oauth2 import BaseStorage
from cbra.ext.oauth2.models import AuthorizationRequestParameters
from cbra.ext.oauth2.models import RefreshToken
from cbra.ext.oauth2.models import ResourceOwner
from cbra.ext.oauth2.types import AuthorizationCode
from cbra.ext.oauth2.types import AuthorizationRequestIdentifier
from cbra.ext.oauth2.types import ResourceOwnerIdentifier
from cbra.ext.oauth2.types import PairwiseIdentifier


T = TypeVar('T', bound=pydantic.BaseModel)


class Storage(BaseStorage, BaseDatastoreRepository):
    __module__: str = 'cbra.ext.google.impl.oauth2'

    def entity_to_model(
        self,
        cls: type[T],
        entity: IDatastoreEntity | None,
        **kwargs: Any
    ) -> T | None:
        if entity is None:
            return None
        return cls.parse_obj({**dict(entity), **kwargs}) # type: ignore

    def model_to_entity(
        self,
        key: IDatastoreKey,
        obj: pydantic.BaseModel,
        exclude: set[str] | None = None
    ) -> IDatastoreEntity:
        # TODO: this is only here to prevent encoding issues with protobuf
        entity = self.entity_factory(key)
        entity.update(json.loads(obj.json(exclude=exclude)))
        return entity

    def __init__(
        self,
        client: Client | Any = cbra.inject('GoogleDatastoreClient')
    ):
        if not isinstance(client, Client):
            raise TypeError(f"Invalid client: {repr(client)}")
        self.client = client

    async def get_authorization_request_by_code(
        self,
        oid: AuthorizationCode
    ) -> AuthorizationRequestParameters | None:
        q = self.query(kind='AuthorizationRequest')
        q.add_filter('code.value', '=', str(oid))
        entity = await self.first(q)
        if entity:
            return self.entity_to_model(
                AuthorizationRequestParameters,
                entity,
                id=entity.key.name
            )

    async def get_authorization_request_by_id(
        self,
        oid: AuthorizationRequestIdentifier
    ) -> AuthorizationRequestParameters | None:
        key = self.key('AuthorizationRequest', str(oid))
        return self.entity_to_model(
            AuthorizationRequestParameters,
            await self.get_entity_by_key(key),
            id=key.name
        )

    async def get_resource_owner(
        self,
        oid: ResourceOwnerIdentifier
    ) -> ResourceOwner | None:
        key = self.key('ResourceOwner', f'clients/{oid.client_id}/subjects/{oid.sub}')
        return self.entity_to_model(
            ResourceOwner,
            await self.get_entity_by_key(key),
        )

    async def persist_authorization_request(self, obj: AuthorizationRequestParameters) -> None:
        entity = self.model_to_entity(self.key('AuthorizationRequest', obj.id), obj)
        await self.put(entity)

    async def persist_ppid(self, obj: PairwiseIdentifier) -> None:
        key = self.key(
            'PairwiseIdentifier',
            await self.allocate('PairwiseIdentifier')
        )
        entity = self.entity_factory(key)
        entity.update({'sector': obj.sector, 'sub': obj.sub})
        await self.put(entity)
        assert entity.key.id is not None
        obj.value = entity.key.id

    async def persist_refresh_token(self, obj: RefreshToken) -> None:
        # TODO: Since we havent implement the AuthorizedGrant yet,
        # simply allocate an id.
        if obj.grant_id == 0:
            obj.grant_id = await self.allocate('AuthorizedGrant')
        key = self.key('RefreshToken', str(obj.token))
        await self.put(self.model_to_entity(key, obj, exclude={'token'}))

    async def persist_resource_owner(self, obj: ResourceOwner) -> None:
        key = self.key('ResourceOwner', f'clients/{obj.client_id}/subjects/{obj.sub}')
        await self.put(self.model_to_entity(key, obj))