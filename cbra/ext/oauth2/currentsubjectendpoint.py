# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.ext.oauth2.models import ClaimSet

from .endpoint import AuthorizationServerEndpoint


class CurrentSubjectEndpoint(AuthorizationServerEndpoint):
    name: str = 'oauth2.me'
    path: str = '/me'
    summary: str = 'Current User Endpoint'

    async def get(self) -> ClaimSet:
        return ClaimSet(sub='allUsers')\
            if not self.is_authenticated()\
            else ClaimSet(sub='self')