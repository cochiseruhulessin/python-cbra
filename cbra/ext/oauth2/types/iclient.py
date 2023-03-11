# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Protocol

from .pairwiseidentifier import PairwiseIdentifier
from .redirecturi import RedirectURI


class IClient(Protocol):
    __module__: str = 'cbra.ext.oauth2.types'
    client_id: str
    sector_identifier: str

    def can_redirect(self, uri: RedirectURI) -> bool: ...
    def get_pairwise_identifier(self, sub: int) -> PairwiseIdentifier: ...
    def get_redirect_uri(self, uri: RedirectURI | None) -> RedirectURI: ...
    def requires_downstream(self) -> bool: ...