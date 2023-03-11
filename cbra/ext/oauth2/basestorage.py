# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
import re
from typing import Any
from typing import TypeVar

from cbra.core.iam.models import Subject
from cbra.types import IDependant
from .models import AuthorizationServerModel
from .models import AuthorizationRequest
from .models import AuthorizationRequestParameters
from .models import AuthorizationState
from .models import Client
from .models import RefreshToken
from .models import ResourceOwner
from .types import AuthorizationCode
from .types import AuthorizationRequestIdentifier
from .types import PairwiseIdentifier


T = TypeVar('T', bound=AuthorizationServerModel)


class BaseStorage(IDependant):
    __module__: str = 'cbra.ext.oauth2'
    pattern: re.Pattern[str] = re.compile(r'(?<!^)(?=[A-Z])')

    async def destroy(self, obj: AuthorizationServerModel) -> None:
        raise NotImplementedError

    async def get(
        self,
        cls: type[T],
        *args: Any,
        **kwargs: Any
    ) -> T | None:
        fn = f"get_{str.lower(self.pattern.sub('_', cls.__name__))}"
        if not hasattr(self, fn):
            raise NotImplementedError(
                f'{type(self).__name__}.{fn}() is not implemented.'
            )
        return await getattr(self, fn)(*args, **kwargs)

    async def get_authorization_request(
        self,
        oid: AuthorizationCode | AuthorizationRequestIdentifier
    ) -> AuthorizationRequest | None:
        params = await self.get(AuthorizationRequestParameters, oid)
        if params is None:
            return None
        return AuthorizationRequest.parse_obj(params)

    @functools.singledispatchmethod
    async def get_authorization_request_parameters(
        self,
        oid: AuthorizationCode | str
    ) -> AuthorizationRequestParameters | None:
        raise NotImplementedError(repr(oid))
    
    @get_authorization_request_parameters.register
    async def _get_authorization_request_by_code(
        self,
        oid: AuthorizationCode
    ) -> AuthorizationRequestParameters | None:
        return await self.get_authorization_request_by_code(oid)
    
    @get_authorization_request_parameters.register
    async def _get_authorization_request_by_id(
        self,
        oid: AuthorizationRequestIdentifier
    ) -> AuthorizationRequestParameters | None:
        return await self.get_authorization_request_by_id(oid)

    async def get_authorization_request_by_code(
        self,
        oid: AuthorizationCode
    ) -> AuthorizationRequestParameters | None: 
        raise NotImplementedError

    async def get_authorization_request_by_id(
        self,
        oid: AuthorizationRequestIdentifier
    ) -> AuthorizationRequestParameters | None: 
        raise NotImplementedError

    async def get_state(self, key: str) -> AuthorizationState | None:
        raise NotImplementedError

    @functools.singledispatchmethod
    async def persist(
        self,
        obj: AuthorizationServerModel | Subject
    ) -> None:
        raise NotImplementedError

    async def persist_authorization_request(
        self,
        obj: AuthorizationRequestParameters
    ) -> None:
        raise NotImplementedError

    async def persist_client(self, obj: Client) -> None:
        raise NotImplementedError
    
    async def persist_ppid(self, obj: PairwiseIdentifier) -> None:
        raise NotImplementedError

    async def persist_refresh_token(
        self,
        obj: RefreshToken
    ) -> None:
            raise NotImplementedError

    async def persist_resource_owner(self, obj: ResourceOwner) -> None:
        raise NotImplementedError

    async def persist_state(self, obj: AuthorizationState) -> None:
        raise NotImplementedError
    
    async def persist_subject(self, obj: Subject) -> None:
        raise NotImplementedError

    @persist.register
    async def _persist_authorization_request(
        self,
        obj: AuthorizationRequestParameters
    ) -> None:
        return await self.persist_authorization_request(obj)

    @persist.register
    async def _persist_client(
        self,
        obj: Client
    ) -> None:
        return await self.persist_client(obj)

    @persist.register
    async def _persist_ppid(
        self,
        obj: PairwiseIdentifier
    ) -> None:
        return await self.persist_ppid(obj)

    @persist.register
    async def _persist_refresh_token(
        self,
        obj: RefreshToken
    ) -> None:
        return await self.persist_refresh_token(obj)

    @persist.register
    async def _persist_resource_owner(
        self,
        obj: ResourceOwner
    ) -> None:
        return await self.persist_resource_owner(obj)

    @persist.register
    async def _persist_state(
        self,
        obj: AuthorizationState
    ) -> None:
        return await self.persist_state(obj)

    @persist.register
    async def _persist_subject(
        self,
        obj: Subject
    ) -> None:
        return await self.persist_subject(obj)