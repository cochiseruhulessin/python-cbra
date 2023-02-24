# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets
from datetime import datetime
from datetime import timezone

import pydantic

from ..types import AuthorizationLifecycle


class Authorization(pydantic.BaseModel):
    """Maintains the lifecycle of an OAuth 2.x/OpenID Connect
    authorization request.
    """
    request_id: str = pydantic.Field(
        default_factory=lambda: secrets.token_bytes(48)
    )

    created: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    status: AuthorizationLifecycle = pydantic.Field(
        default=AuthorizationLifecycle.requested
    )