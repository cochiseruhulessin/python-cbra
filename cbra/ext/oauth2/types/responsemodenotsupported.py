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


class ResponseModeNotSupported(Abortable):
    status_code: int = 400

    def __init__(self, mode: str):
        self.mode = mode

    async def as_response(self) -> fastapi.Response:
        return fastapi.responses.PlainTextResponse(
            content=f'Response mode {self.mode} is not supported by this server.'
        )