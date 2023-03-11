# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import Abortable
from .redirecturi import RedirectURI


class AuthorizationException(Abortable):
    __module__: str = 'cbra.ext.oauth2.types'
    error: str
    iss: str
    message: str
    redirect_uri: RedirectURI
    state: str | None
    status_code: int = 303

    def __init__(
        self,
        redirect_uri: RedirectURI,
        iss: str,
        state: str | None = None
    ):
        self.iss = iss
        self.redirect_uri = redirect_uri
        self.state = state

    async def as_response(self) -> fastapi.Response:
        return fastapi.Response(
            status_code=self.status_code,
            headers={'Location': self.get_redirect_uri()}
        )
    
    def get_redirect_uri(self) -> str:
        params: dict[str, str] = {
            'error': self.error,
            'error_description': self.message,
            'iss': self.iss
        }
        if self.state:
            params['state'] = self.state
        return self.redirect_uri.redirect(**params)