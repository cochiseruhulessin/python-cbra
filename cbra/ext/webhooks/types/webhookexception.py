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
from .webhookresponse import WebhookResponse


class WebhookException(Abortable):
    __module__: str = 'cbra.ext.webhooks'
    status_code: int = 200
    code: str
    reason: str

    async def as_response(self) -> fastapi.responses.JSONResponse:
        return fastapi.responses.JSONResponse(
            status_code=self.status_code,
            content=WebhookResponse(
                code=self.code,
                reason=self.reason,
                accepted=False,
                success=False
            ).dict()
        )
