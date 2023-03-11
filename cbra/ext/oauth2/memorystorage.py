# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import random
from typing import cast
from typing import Any
from typing import TypeVar

from cbra.core.iam import MemorySubjectRepository
from cbra.core.iam.models import Subject
from .basestorage import BaseStorage
from .models import AuthorizationRequestParameters
from .models import AuthorizationState
from .models import AuthorizationServerModel
from .models import Client
from .models import RefreshToken
from .models import ResourceOwner
from .types import AuthorizationCode
from .types import AuthorizationRequestIdentifier
from .types import PairwiseIdentifier


T = TypeVar('T')


class MemoryStorage(BaseStorage):
    """An in-memory implementation of :class:`~cbra.ext.oauth2.BaseStorage`."""
    __module__: str = 'cbra.ext.oauth2'
    objects: dict[str, dict[Any, Any]] = collections.defaultdict(dict)
    subjects: MemorySubjectRepository = MemorySubjectRepository()

    @classmethod
    def clear(cls) -> None:
        cls.objects = collections.defaultdict(dict)

    def __init__(self):
        self.objects = MemoryStorage.objects

    async def destroy(self, obj: AuthorizationServerModel) -> None:
        self.objects[type(obj).__name__].pop(obj.__key__[0][1], None) # type: ignore

    async def get_authorization_request_by_id(
        self,
        oid: AuthorizationRequestIdentifier
    ) -> AuthorizationRequestParameters | None:
        return self._get(AuthorizationRequestParameters, oid)
    
    async def get_authorization_request_by_code(
        self,
        oid: AuthorizationCode
    ) -> AuthorizationRequestParameters | None:
        for params in self.objects[AuthorizationRequestParameters.__name__].values():
            if not isinstance(params, AuthorizationRequestParameters):
                continue
            if params.code is None or params.code.value != oid:
                continue
            break
        else:
            params = None
        return params

    async def get_resource_owner(self, id: int) -> ResourceOwner | None:
        return self._get(ResourceOwner, id)

    async def get_state(self, key: str) -> AuthorizationState | None:
        return self._get(AuthorizationState, key)

    async def persist_authorization_request(self, obj: AuthorizationRequestParameters) -> None:
        assert obj.id is not None
        self.objects[type(obj).__name__][obj.id] = obj

    async def persist_client(self, obj: Client) -> None:
        self.objects[type(obj).__name__][obj.client_id] = obj

    async def persist_ppid(self, obj: PairwiseIdentifier) -> None:
        obj.value = random.randint(10**9, (10**10) - 1)
        self.objects[type(obj).__name__][obj.value] = obj

    async def persist_refresh_token(self, obj: RefreshToken) -> None:
        self.objects[type(obj).__name__][obj.token] = obj

    async def persist_resource_owner(self, obj: ResourceOwner) -> None:
        self.objects[type(obj).__name__][obj.id] = obj

    async def persist_state(self, obj: AuthorizationState) -> None:
        self.objects[type(obj).__name__][obj.state] = obj

    async def persist_subject(self, obj: Subject) -> None:
        await self.subjects.persist(obj) # type: ignore

    def _get(self, Model: type[T], key: int | str) -> T | None:
        return cast(Model, self.objects[Model.__name__].get(key))