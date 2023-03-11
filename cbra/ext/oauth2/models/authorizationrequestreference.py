# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic

from ..types import AuthorizationRequestIdentifier
from ..types import FatalAuthorizationException
from .authorizationrequestparameters import AuthorizationRequestParameters


class AuthorizationRequestReference(pydantic.BaseModel):
    client_id: str
    request_uri: str
    remote_host: str

    @property
    def id(self) -> str:
        return AuthorizationRequestIdentifier(str.split(self.request_uri, ':')[-1])

    async def load(
        self,
        client: Any,
        storage: Any,
        session_id: str
    ) -> AuthorizationRequestParameters:
        params = await storage.get(AuthorizationRequestParameters, self.id)
        if params is None:
            raise FatalAuthorizationException("The request does not exist.")
        return params