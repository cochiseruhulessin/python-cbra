# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

from cbra.types import Forbidden
from cbra.types import NullPrincipal
from cbra.core import Endpoint

from .googleserviceaccountprincipal import GoogleServiceAccountPrincipal


class GoogleEndpoint(Endpoint):
    """A :class:`~cbra.core.Endpoint` implementation that is invoked
    by Google, for example by services such as Eventarc with Cloud Run,
    Cloud Tasks or Pubsub.
    """
    __abstract__: bool = True
    __module__: str = 'cbra.ext.google'
    allowed_service_accounts: set[str] = set()
    if os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL'):
        allowed_service_accounts = {os.environ['GOOGLE_SERVICE_ACCOUNT_EMAIL']}
    principal: GoogleServiceAccountPrincipal | NullPrincipal # type: ignore
    require_authentication: bool = True
    trusted_providers: set[str] = {
        "https://accounts.google.com"
    }

    async def authenticate(self) -> None:
        await super().authenticate()
        if not self.ctx.is_authenticated():
            return
        if self.ctx.subject.email not in self.allowed_service_accounts:
            self.logger.critical(
                'Google service endpoint was invoked with a disallowed '
                'service account (email: %s)',
                self.ctx.subject.email
            )
            raise Forbidden