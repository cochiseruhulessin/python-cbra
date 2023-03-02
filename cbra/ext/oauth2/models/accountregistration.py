# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone

import pydantic
from canonical import EmailAddress

from cbra.types import PersistedModel


ALLOWED_DOMAINS: set[str] = {
    'gmail.com',
    'outlook.com',
    'hotmail.com',
    'live.com',
    'myyahoo.com',
    'yahoo.com',
    'rocketmail.com',
    'icloud.com',
    'pm.me',
    'protonmail.com'
}


class AccountRegistration(PersistedModel):
    """Retains the state of an account registration request that
    requires a backup email address.

    Registration of a new account is done by verifying an email address
    using a shared secret (verification code). If the email adres is not
    whitelist per its domain, then a fallback email address must be
    provided. The :class:`AccountRegistration` model must then resolve
    either of three cases:

    - Both email addresses are not linked to existing accounts. In this
      case, an account that owns both addresses is created.
    - One address is linked to an existing account. The other address is
      then also added to the account.
    - The email addresses are linked to different accounts. This is an
      error state.
    """
    id: int | None = pydantic.Field(
        default=None,
        auto_assign=True
    )

    requested: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    register: EmailAddress = pydantic.Field(
        default=...,
        primary_key=True
    )
    fallback: EmailAddress | None = None