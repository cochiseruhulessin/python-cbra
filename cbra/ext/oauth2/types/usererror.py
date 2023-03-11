# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import fastapi

from cbra.core.conf import settings
from cbra.types import Abortable


class UserError(Abortable):
    __module__: str = 'cbra.ext.oauth2.types'
    authorization_url: str
    error: str
    request_id: str

    def __init__(
        self,
        error: str,
        request_id: str,
        authorize: str,
    ):
        self.authorization_url = authorize
        self.error = error
        self.request_id = request_id

    async def as_response(self) -> fastapi.Response:
        p: dict[str, str] = {
            'error': self.error,
            'next': self.authorization_url,
            'request': self.request_id
        }
        q = urllib.parse.urlencode(p, quote_via=urllib.parse.quote)
        return fastapi.responses.RedirectResponse(
            status_code=303,
            url=f'{settings.OAUTH2_ERROR_URL}?{q}'
        )