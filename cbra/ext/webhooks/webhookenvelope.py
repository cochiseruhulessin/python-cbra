# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from types import NotImplementedType

import pydantic
from cbra.types import IDependant
from cbra.types import IVerifier
from cbra.types import Request


class WebhookEnvelope(IDependant):
    __module__: str = 'cbra.ext.webhooks'
    event_name: str | NotImplementedType = NotImplementedType
    logger: logging.Logger = logging.getLogger('cbra.endpoint.webhooks')

    def get_message(self) -> pydantic.BaseModel:
        raise NotImplementedError

    async def verify(
        self,
        request: Request,
        verifier: IVerifier
    ) -> bool:
        """Subclasses must override this method to verify the authenticity "
        and integrity of the webhook message.
        """
        raise NotImplementedError("Subclasses must override this method.")