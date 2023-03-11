# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import EmailAddress


class SessionClaims(pydantic.BaseModel):
    ctx: str | None = None
    uid: int | None = None
    iss: str | None = None
    sub: str | None = None
    email: EmailAddress | None = None
    auth_time: int | None = None