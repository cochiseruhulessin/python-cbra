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


class FatalAuthorizationException(Abortable):
    __module__: str = 'cbra.ext.oauth2.types'
    status_code: int = 400

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

    async def as_response(self) -> fastapi.Response:
        return fastapi.responses.PlainTextResponse(
            status_code=self.status_code,
            content=self.message
        )