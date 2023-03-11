# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

import cbra.core as cbra
from cbra.core.iam.models import SubjectClaimSet
from cbra.types import IDependant
from cbra.types import IDeferred
from ..models import Grant
from ..models import ResourceOwner
from ..types import IAuthorizationServerStorage
from .requestedgrant import RequestedGrant


class RequestResourceOwner(IDependant, IDeferred):
    __module__: str = 'cbra.ext.oauth2.params'
    _claims: SubjectClaimSet
    _grant: Grant
    _owner: ResourceOwner
    _storage: IAuthorizationServerStorage

    def __init__(
        self,
        grant: Grant = RequestedGrant,
        storage: IAuthorizationServerStorage = cbra.instance('_AuthorizationServerStorage'),
    ):
        self._grant = grant
        self._storage = storage

    async def initialize(self) -> None:
        pass