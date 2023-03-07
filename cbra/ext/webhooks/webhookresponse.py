# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class WebhookResponse(pydantic.BaseModel):
    accepted: bool = pydantic.Field(
        default=...,
        title="Accepted?",
        description='Indicates if the server accepted the webhook.'
    )
    success: bool = pydantic.Field(
        default=...,
        title="Succes?",
        description='Indicates if the server succesfully processed the message.'
    )

    reason: str | None = pydantic.Field(
        default=None,
        title="Reason",
        description='Describes why the webhook message was not accepted.'
    )