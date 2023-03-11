# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from headless.ext.oauth2.types import GrantType

from ..types import ClientAuthenticationMethod
from ..types import OIDCProvider
from ..types import PairwiseIdentifier
from ..types import RedirectURI
from ..types import RefreshTokenPolicyType
from .applicationclient import ApplicationClient


class Client(pydantic.BaseModel):
    __root__: ApplicationClient

    @property
    def access_token_ttl(self) -> int | None:
        return None

    @property
    def auth_method(self) -> ClientAuthenticationMethod:
        return self.__root__.token_endpoint_auth_method

    @property
    def client_id(self) -> str:
        return self.__root__.client_id

    @property
    def client_secret(self) -> str | None:
        return self.__root__.client_secret

    @property
    def refresh_token_policy(self) -> RefreshTokenPolicyType:
        return self.__root__.refresh_token_policy

    @property
    def refresh_token_ttl(self) -> int:
        return self.__root__.refresh_token_ttl

    @property
    def sector_identifier(self) -> str:
        return self.__root__.sector_identifier

    def can_grant(self, grant_type: GrantType) -> bool:
        return self.__root__.can_grant(grant_type)

    def can_redirect(self, uri: RedirectURI) -> bool:
        return self.__root__.can_redirect(uri)

    def can_use(self, scope: set[str]) -> bool:
        return self.__root__.can_use(scope)

    def get_redirect_uri(self, uri: RedirectURI | None) -> RedirectURI:
        return self.__root__.get_redirect_uri(uri)
    
    def get_pairwise_identifier(self, sub: int) -> PairwiseIdentifier:
        return self.__root__.get_pairwise_identifier(sub)

    def requires_downstream(self) -> bool:
        return self.__root__.requires_downstream()
    
    def get_provider(self) -> OIDCProvider:
        return self.__root__.get_provider()
    
    def is_confidential(self) -> bool:
        return self.auth_method != ClientAuthenticationMethod.none