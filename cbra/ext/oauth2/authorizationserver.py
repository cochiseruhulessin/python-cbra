# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import cbra.core as cbra
from cbra.core.conf import settings
from .applicationstorage import ApplicationStorage
from .authorizationendpoint import AuthorizationEndpoint
from .authorizationserverstorage import AuthorizationServerStorage
from .callbackendpoint import CallbackEndpoint
from .currentsubjectendpoint import CurrentSubjectEndpoint
from .endpoint import AuthorizationServerEndpoint
from .frontendloginendpoint import FrontendLoginEndpoint
from .frontendredirectionendpoint import FrontendRedirectionEndpoint
from .loginendpoint import LoginEndpoint
from .metadataendpoint import MetadataEndpoint
from .onboardingendpoint import OnboardingEndpoint
from .tokenendpoint import TokenEndpoint
from .tokenhandlerendpoint import TokenHandlerEndpoint
from .types import ResponseType


class AuthorizationServer(cbra.APIRouter):
    __module__: str = 'cbra.ext.oauth2'
    client: dict[str, Any] | None
    iss: str | None
    handlers: set[type[AuthorizationServerEndpoint | TokenHandlerEndpoint]] = set()
    response_types: list[ResponseType]
    storage_class: type[AuthorizationServerStorage]

    def __init__(
        self,
        response_types: list[ResponseType] | None,
        iss: str | None = None,
        client: dict[str, Any] | None = None,
        storage_class: type[AuthorizationServerStorage] = AuthorizationServerStorage,
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs) # type: ignore
        self.client = client
        self.iss = iss
        self.response_types = response_types or []
        self.storage_class = storage_class

        # Determine which request handlers we must add to the authorization
        # server.
        self.handlers = {
            CurrentSubjectEndpoint,
            FrontendLoginEndpoint,
            FrontendRedirectionEndpoint,
            LoginEndpoint,
            MetadataEndpoint,
            OnboardingEndpoint
        }

        # If there is any response type, this indicates that the
        # server must provide an authorization endpoint.
        if response_types:
            self.handlers.add(AuthorizationEndpoint)
            self.handlers.add(CallbackEndpoint)
            self.handlers.add(TokenEndpoint)

    def add_to_router(self, router: cbra.Application, *args: Any, **kwargs: Any):
        self.container = router.container
        self.container.provide('_LocalClient', {
            'qualname': '_',
            'symbol': lambda: self.client
        })
        self.container.provide('_ApplicationStorage', {
            'qualname': f'{ApplicationStorage.__module__}.{ApplicationStorage.__name__}',
            'symbol': ApplicationStorage
        })
        self.container.provide('_AuthorizationServerStorage', {
            'qualname': f'{self.storage_class.__module__}.{self.storage_class.__name__}',
            'symbol': self.storage_class
        })
        self.container.provide('AuthorizationServerStorage', {
            'qualname': settings.OAUTH2_STORAGE
        })
        for handler in sorted(self.handlers, key=lambda x: x.__name__):
            self.add(handler, path=handler.path)
        return super().add_to_router(router, *args, **kwargs)