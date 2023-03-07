# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class IncomingWebhook(pydantic.BaseModel):
    """Maintains all information needed to create, re-create webhooks
    with external services and verify the incoming messages.
    """
    id: str

    #: The name of the service sending the webhook messages.
    sender: str

    #: If the service allows creation of webhooks through an
    #: HTTP API, the URL of the corresponding webhook resource.
    url: str | None = None