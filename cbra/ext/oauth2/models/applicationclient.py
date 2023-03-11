# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any
from typing import Literal

import pydantic
from headless.ext.oauth2.types import GrantType

from ..types import ClientAuthenticationMethod
from ..types import FatalAuthorizationException
from ..types import PairwiseIdentifier
from ..types import RedirectURI
from ..types import RefreshTokenPolicyType
from .baseclient import BaseClient
from .downstreamproviderconfig import DownstreamProviderConfig


class ApplicationClient(BaseClient):
    """An OAuth 2.0 that is a specific application."""
    allowed_redirect_uris: list[RedirectURI] = pydantic.Field(
        default=...,
        min_length=1
    )
    client_id: str
    client_secret: str | None = None
    downstream: DownstreamProviderConfig = pydantic.Field(
        default_factory=DownstreamProviderConfig
    )
    grant_types: list[GrantType] = []
    kind: Literal['Application']
    refresh_token_ttl: int
    refresh_token_policy: RefreshTokenPolicyType = RefreshTokenPolicyType.static
    scope: set[str] = set()
    sector_identifier: str
    sector_identifier_uri: str | None = None
    token_endpoint_auth_method: ClientAuthenticationMethod

    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        # When pairwise Subject Identifiers are used, the OpenID Provider
        # MUST calculate a unique sub (subject) value for each Sector
        # Identifier. The Subject Identifier value MUST NOT be reversible
        # by any party other than the OpenID Provider.
        #
        # Providers that use pairwise sub values and support Dynamic
        # Client Registration [OpenID.Registration] SHOULD use the
        # sector_identifier_uri parameter. It provides a way for a group
        # of websites under common administrative control to have consistent
        # pairwise sub values independent of the individual domain names.
        # It also provides a way for Clients to change redirect_uri
        # domains without having to reregister all of their users.
        #
        # If the Client has not provided a value for sector_identifier_uri
        # in Dynamic Client Registration [OpenID.Registration], the Sector
        # Identifier used for pairwise identifier calculation is the host
        # component of the registered redirect_uri. If there are multiple
        # hostnames in the registered redirect_uris, the Client MUST register
        # a sector_identifier_uri.
        #
        # When a sector_identifier_uri is provided, the host component of
        # that URL is used as the Sector Identifier for the pairwise identifier
        # calculation. The value of the sector_identifier_uri MUST be a URL
        # using the https scheme that points to a JSON file containing an
        # array of redirect_uri values. The values of the registered
        # redirect_uris MUST be included in the elements of the array.
        #
        # OpenId Connect Core 1.0, Section 8.1
        redirect_uris: list[str] = values.get('allowed_redirect_uris') or []
        sector_identifier: str | None = values.get('sector_identifier')
        sector_identifier_uri: str | None = values.get('sector_identifier_uri')
        redirect_hosts = set(
            filter(
                bool,
                [urllib.parse.urlparse(uri).hostname for uri in redirect_uris]
            )
        )
        if len(redirect_uris) == 0:
            raise ValueError("at least one redirect URI must be provided.")
        if not sector_identifier:
            if sector_identifier_uri is None:
                if len(redirect_hosts) > 1:
                    raise ValueError(
                        "sector_identifier or sector_identifier_uri must be "
                        "provided with multiple redirects URIs"
                    )
                sector_identifier = redirect_hosts.pop()
            else:
                assert isinstance(sector_identifier_uri, str)
                p = urllib.parse.urlparse(sector_identifier_uri)
                if not p.hostname:
                    raise ValueError('sector_identifier_uri does not contain a hostname.')
                sector_identifier = p.hostname
        values['sector_identifier'] = sector_identifier
        return values

    def can_grant(self, grant_type: GrantType) -> bool:
        return grant_type in self.grant_types

    def can_redirect(self, uri: RedirectURI) -> bool:
        """Return a boolean indicating if the client allows redirection
        to the given URI.
        """
        return uri in self.allowed_redirect_uris

    def can_use(self, scope: set[str]) -> bool:
        return scope <= self.scope

    def get_pairwise_identifier(self, sub: int) -> PairwiseIdentifier:
        return PairwiseIdentifier(self.sector_identifier, sub)

    def get_redirect_uri(self, uri: RedirectURI | None) -> RedirectURI:
        if len(self.allowed_redirect_uris) > 1:
            raise NotImplementedError
        uri = uri or self.allowed_redirect_uris[0]
        if uri not in self.allowed_redirect_uris:
            raise FatalAuthorizationException(
                "The client does not allow redirection to the given "
                "redirect_uri.",
                status_code=403
            )
        return RedirectURI(uri or self.allowed_redirect_uris[0])

    def requires_downstream(self) -> bool:
        return self.downstream.required

    def get_provider(self):
        assert self.downstream.providers
        if len(self.downstream.providers) > 1:
            raise NotImplementedError
        return self.downstream.providers[0]