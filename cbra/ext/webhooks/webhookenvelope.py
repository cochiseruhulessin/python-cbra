# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Awaitable

from cbra.types import IVerifier
from cbra.types import Request


class WebhookEnvelope:
    __module__: str = 'cbra.ext.webhooks'

    @property
    def event_name(self) -> str:
        return self.get_event_name()
    
    def get_event_name(self) -> str:
        """Subclasses must override this method to return the event name
        of the incoming message.
        """
        raise NotImplementedError("Subclasses must override this method.")
    

    def verify(
        self,
        request: Request,
        verifier: IVerifier
    ) -> Awaitable[bool]:
        """Subclasses must override this method to verify the authenticity "
        and integrity of the webhook message.
        """
        raise NotImplementedError("Subclasses must override this method.")